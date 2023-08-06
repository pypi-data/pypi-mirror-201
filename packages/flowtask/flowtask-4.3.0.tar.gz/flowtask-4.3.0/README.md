# FlowTask DataIntegration #

FlowTask DataIntegration is a plugin-based, component-driven task execution framework for create complex Tasks.

FlowTask runs Tasks defined in JSON, YAML or TOML files, any Task is a combination of Components,
and every component in the Task run sequentially or depend of others, like a DAG.

Can create a Task combining Commands, Shell scripts and other specific Components (as TableInput: Open a Table using a datasource, DownloadFromIMAP: Download a File from a IMAP Folder, and so on), any Python Callable can be a Component inside a Task, or can extends UserComponent to build your own componets.

Every designed Task can run from CLI, programmatically, via RESTful API (using our aioHTTP-based Handler), called by WebHooks or even dispatched to a external Worker using our built-in Scheduler.

## Quickstart ##

```console
pip install flowtask
```

Tasks can organizated into directory structure like this:

tasks /
    ├── programs /
      ├── test /
           ├── tasks /

The main reason of this structure, is maintain organized several tasks by tenant/program, avoiding filling a directory with several task files.

FlowTask support "TaskStorage", a Task Storage is the main repository for tasks, main Task Storage is a directory in any filesystem path (optionally you can syncronize that path using git), but Tasks can be saved onto a Database or a S3 bucket.

## Dependencies ##

 * aiohttp (Asyncio Web Framework and Server) (required by navigator)
 * AsyncDB
 * QuerySource
 * Navigator-api
 * (Optional) Qworker (for distributing asyncio Tasks on distributed workers).

## Features ##

* Component-based Task execution framework with several components covering several actions (download files, create pandas dataframes from files, mapping dataframe columns to a json-dictionary, etc)
* Built-in API for execution of Tasks.

### How I run a Task? ###

Can run a Task from CLI:
```console
task --program=test --task=example
```

on CLI, you can pass an ENV (enviroment) to change the environment file on task execution.
```console
ENV=dev task --program=test --task=example
```

or Programmatically:
```python
from flowtask import Task
import asyncio

task = Task(program='test', task='example')
results = asyncio.run(task.run())
# we can alternatively, using the execution mode of task object:
results = asyncio.run(task())
```

### Requirements ###

* Python >= 3.9
* asyncio (https://pypi.python.org/pypi/asyncio/)
* aiohttp >= 3.6.2

### Contribution guidelines ###

Please have a look at the Contribution Guide

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

### License ###

Navigator is licensed under Apache 2.0 License. See the LICENSE file for more details.
