import asyncio
import copy
from typing import (
    Dict,
    List
)
from collections.abc import Callable
import pandas as pd
from navconfig.conf import asyncpg_url
from navconfig.logging import logging
from asyncdb import AsyncDB
from asyncdb.exceptions import NoDataFound
from flowtask.exceptions import (
    ComponentError
)
from flowtask.parsers.maps import open_map, open_model
import flowtask.components.TransformRows.functions as tfunctions
from flowtask.utils.executor import getFunction
from .abstract import DtComponent

class tMap(DtComponent):
    """
    tMap.

         Overview

        Component to get a Table (or query) into a Pandas Dataframe (using SQL Alchemy)

    .. table:: Properties
       :widths: auto


    +--------------+----------+-----------+-------------------------------------------------------+
    | Name         | Required | Summary                                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  __init__    |   Yes    | This attribute is to initialize the component methods             |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  column_info |   Yes    | I access the information of the column through a statement in     |
    |              |          | sql to extract the data                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  clean_names |   Yes    | Remove duplicate names from data                                  |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  start       |   Yes    | We initialize the component obtaining the data through the        |
    |              |          | through the parameter type                                        |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  close       |   Yes    | The close method of a file object flushes any unwritten data and  |
    |              |          | closes the file object                                            |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  run         |   Yes    | This method executes the function                                 |
    +--------------+----------+-----------+-------------------------------------------------------+


    Return the list of arbitrary days
    """
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        self.tablename: str = None
        self.schema: str = None
        self.model: str = None
        self._modelinfo: Dict = None
        self.map: str = None
        self._mapping: Dict = None
        self.force_map: bool = False
        self.replace_columns: bool = True
        self.drop_missing: bool = False
        super(tMap, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        if not self.schema:
            self.schema = self._program
        # use it for getting column information
        if 'flavor' in kwargs:
            self._flavor = kwargs['flavor']
            del kwargs['flavor']
        else:
            self._flavor = 'postgres'

    async def column_info(
            self,
            table: str,
            schema: str = 'public',
            flavor: str = 'postgres'
        ) -> List:
        if not self.force_map:
            result = None
            if flavor == 'postgres':
                tablename = f'{schema}.{table}'
                discover = f"""SELECT attname AS column_name, atttypid::regtype AS data_type, attnotnull::boolean as notnull
                  FROM pg_attribute WHERE attrelid = '{tablename}'::regclass AND attnum > 0 AND NOT attisdropped ORDER  BY attnum;
                """
                try:
                    db = AsyncDB('pg', dsn=asyncpg_url)
                    async with await db.connection() as conn:
                        result, error = await conn.query(discover)
                        if error:
                            raise ComponentError(
                                f'Column Info Error {error}'
                            )
                except NoDataFound:
                    pass
                finally:
                    db = None
            else:
                raise ValueError(
                    f"Column Info: Flavor not supported yet: {flavor}"
                )
            if result:
                return {item['column_name']: item['data_type'] for item in result}
        # getting model from file:
        model = await open_model(table, schema)
        if model:
            fields = model['fields']
            return {field: fields[field]['data_type'] for field in fields}
        else:
            if self.force_map:
                self._logger.debug(
                    f'Open Map: Forcing using of Map File {schema}.{table}'
                )
            else:
                self._logger.error(
                    f"Open Map: Table {schema}.{table} doesn't exist"
                )
            return None

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        # getting model from model or from tablename
        if self.tablename:
            self._modelinfo = await self.column_info(
                table=self.tablename,
                schema=self.schema,
                flavor=self._flavor
            )
        try:
            # open a map file:
            self._mapping = await open_map(filename=str(self.map), program=self._program)
        except Exception as err:
            raise ComponentError(
                f"TableMap: Error open Map File: {err}"
            ) from err


    async def close(self):
        """
        close.

            close method
        """

    def is_dataframe(self, df) -> bool:
        return isinstance(df, pd.DataFrame)

    async def run(self):
        """
        run.

            Iteration over all dataframes.
        """
        if isinstance(self.data, list): # a list of dataframes
            pass
        elif isinstance(self.data, dict): # named queries
            pass
        else:
            # one single dataframe
            if not self.is_dataframe(self.data):
                raise ComponentError(
                    "tMap Error: we're expecting a Pandas Dataframe as source."
                )
            # adding first metrics:
            self.add_metric('started_rows', self.data.shape[0])
            self.add_metric('started_columns', self.data.shape[1])
            df = await self.transform(self.data, copy.deepcopy(self._mapping))
            # check if a column is missing:
            if self.drop_missing is True:
                for column in df.columns:
                    if column not in self._mapping: # Dropping unused columns
                        df.drop(column, axis='columns', inplace=True)
            self._result = df
            # avoid threat the Dataframe as a Copy
            self._result.is_copy = None
            return self._result

    async def transform(self, df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
        it = df.copy()
        for column, field in mapping.items():
            logging.debug(f'tMap: CALLING {column} for {field}')
            if isinstance(field, str): # making a column replacement
                try:
                    if column != field:
                        it[column] = it[field]
                        it.drop(field, axis='columns', inplace=True)
                    continue
                except KeyError:
                    self._logger.error(f'Column doesn\'t exists: {field}')
                    continue
            elif isinstance(field, dict):
                # direct calling of Transform Function
                operation = field['value']
                fname = operation.pop(0)
                # only calls functions on TransformRows scope:
                try:
                    kwargs = operation[0]
                except IndexError:
                    kwargs = {}
                it = await self.call_function(fname, it, column, args=kwargs)
            else:
                col = field.pop(0)
                if len(field) == 0:
                    # there is no change to made:
                    # simple field replacement
                    it[column] = it[col]
                    continue
                elif len(field) == 1:
                    fname = field.pop(0)
                    try:
                        kwargs = field[1]
                    except IndexError:
                        kwargs = {}
                    # first, if col <> column, we need to rename it
                    it[column] = it[col]
                    if self.replace_columns is True:
                        it.drop(col, axis='columns', inplace=True)
                    # only calls functions on TransformRows scope:
                    it = await self.call_function(fname, it, column, args=kwargs)
                else:
                    # the same, if col <> column, we need to rename it
                    if isinstance(col, list):
                        ### combine several columns into one
                        it[column] = it[col].apply(" ".join, axis=1)
                        # is a list of columns:
                        fname = field.pop(0)
                        try:
                            kwargs = field[0]
                        except IndexError:
                            kwargs = {}
                        try:
                            print('CALLING >> ', fname, column, kwargs)
                            it = await self.call_function(fname, it, column, args=kwargs)
                        except Exception:
                            pass
                        # func = getFunction(fname)
                        # if callable(func):
                        #     print('CALLING FUNC ', func, 'FOR COL ', column, col)
                        #     try:
                        #         result = func(col, **kwargs)
                        #     except (KeyError, IndexError, ValueError):
                        #         result = func()
                        #     r = {
                        #         column: result
                        #     }
                        #     it = it.assign(**r)
                        #     it = it.copy()
                    else:
                        it[column] = it[col]
                        if self.replace_columns is True:
                            if column != col:
                                it.drop(col, axis='columns', inplace=True)
                        # iterate over all functions in field
                        for fname in field:
                            if isinstance(fname, str):
                                it = await self.call_function(fname, it, column, args={})
                            elif isinstance(fname, list):
                                fn = fname[0]
                                try:
                                    kwargs = fname[1]
                                except IndexError:
                                    kwargs = {}
                                it = await self.call_function(fn, it, column, args=kwargs)

         # at the end
        df = it
        if self._debug is True:
            columns = list(df.columns)
            print('=== tMap Columns ===')
            for column in columns:
                t = df[column].dtype
                print(column, '->', t, '->', df[column].iloc[0])
            print('===')
            print(df)
        # avoid threat the Dataframe as a Copy
        df.is_copy = None
        try:
            self.add_metric('mapped_rows', df.shape[0])
            self.add_metric('mapped_columns', df.shape[1])
        except Exception as err: # pylint: disable=W0703
            logging.error(
                f'TransformRows: Error setting Metrics: {err}'
            )
        return df

    async def call_function(
            self,
            fname: str,
            df: pd.DataFrame,
            column: str,
            args: Dict = None
        ) -> pd.DataFrame:
        logging.debug(
            f'tMap: Calling Fn {fname!s} for {column} with args: {args}'
        )
        try:
            func = getattr(tfunctions, fname)
        except AttributeError:
            func = globals()[fname]
        if callable(func):
            if fname == 'fill_column':
                args['variables'] = self._variables
            if args:
                it = func(df=df, field=column, **args)
            else:
                it = func(df=df, field=column)
            return it
        else:
            logging.warning(f'tMap: Function {func} is not callable.')
            return df
