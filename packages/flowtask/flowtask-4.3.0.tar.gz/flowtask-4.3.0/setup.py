#!/usr/bin/env python
"""flowtask.

    Framework for Task orchestation.
See:
 https://github.com/phenobarbital/flowtask
"""
import ast
from os import path

from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup


def get_path(filename):
    """get_path.
    Get relative path for a file.
    """
    return path.join(path.dirname(path.abspath(__file__)), filename)


def readme():
    """readme.
    Get the content of README file.
    Returns:
        str: string of README file.
    """
    with open(get_path('README.md'), encoding='utf-8') as file:
        return file.read()


version = get_path('flowtask/version.py')
with open(version, 'r', encoding='utf-8') as meta:
    # exec(meta.read())
    t = compile(meta.read(), version, 'exec', ast.PyCF_ONLY_AST)
    for node in (n for n in t.body if isinstance(n, ast.Assign)):
        if len(node.targets) == 1:
            name = node.targets[0]
            if isinstance(name, ast.Name) and \
                name.id in (
                    '__version__',
                    '__title__',
                    '__description__',
                    '__author__',
                    '__license__', '__author_email__'):
                v = node.value
                if name.id == '__version__':
                    __version__ = v.s
                if name.id == '__title__':
                    __title__ = v.s
                if name.id == '__description__':
                    __description__ = v.s
                if name.id == '__license__':
                    __license__ = v.s
                if name.id == '__author__':
                    __author__ = v.s
                if name.id == '__author_email__':
                    __author_email__ = v.s


COMPILE_ARGS = ["-O2"]

extensions = [
    Extension(
        name='flowtask.exceptions',
        sources=['flowtask/exceptions.pyx'],
        extra_compile_args=COMPILE_ARGS,
    ),
    Extension(
        name='flowtask.parsers.base',
        sources=['flowtask/parsers/base.pyx'],
        extra_compile_args=COMPILE_ARGS,
    ),
    Extension(
        name='flowtask.parsers._yaml',
        sources=['flowtask/parsers/_yaml.pyx'],
        extra_compile_args=COMPILE_ARGS,
    ),
    Extension(
        name='flowtask.parsers.json',
        sources=['flowtask/parsers/json.pyx'],
        extra_compile_args=COMPILE_ARGS,
    ),
    Extension(
        name='flowtask.parsers.toml',
        sources=['flowtask/parsers/toml.pyx'],
        extra_compile_args=COMPILE_ARGS,
    ),
    Extension(
        name='flowtask.utils.parserqs',
        sources=['flowtask/utils/parseqs.pyx'],
        extra_compile_args=COMPILE_ARGS,
    ),
    Extension(
        name='flowtask.utils.json',
        sources=['flowtask/utils/json.pyx'],
        extra_compile_args=COMPILE_ARGS,
        language="c++"
    ),
    Extension(
        name='flowtask.types.typedefs',
        sources=['flowtask/types/typedefs.pyx'],
        extra_compile_args=COMPILE_ARGS
    ),
    Extension(
        name='flowtask.utils.functions',
        sources=['flowtask/utils/functions.pyx'],
        extra_compile_args=COMPILE_ARGS,
        language="c++"
    ),
]


setup(
    name='flowtask',
    version=__version__,
    python_requires=">=3.9.16",
    url='https://github.com/phenobarbital/flowtask',
    description=__description__,
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: BSD License",
        "Framework :: AsyncIO",
    ],
    author='Jesus Lara',
    author_email='jlara@trocglobal.com',
    packages=find_packages(exclude=['contrib', 'bin', 'settings']),
    keywords="DataIntegration DataIntegration Task Orchestation Framework Task-Runner, Pipelines",
    platforms=["*nix"],
    license='Apache License 2.0',
    setup_requires=[
        "wheel==0.38.4",
        "Cython==0.29.33",
        "asyncio==3.4.3",
    ],
    install_requires=[
        'asyncio==3.4.3',
        'uvloop==0.17.0',
        'borax==3.5.0',
        'PyDrive==1.3.1',
        'tqdm==4.63.0',
        'asyncssh[bcrypt,fido2,libnacl,pkcs11,pyOpenSSL]==2.13.1',
        'pyxlsb==1.0.8',
        'pyecharts==1.9.0',
        'jsonschema==4.17.3',
        'snapshot-selenium==0.0.2',
        'webdriver-manager==3.5.2',
        'aioimaplib==1.0.1',
        'msal==1.21.0',
        'adal==1.2.7',
        'openpyxl==3.1.0',
        'xlrd==2.0.1',
        'zeep==4.1.0',
        'nltk==3.7',
        'jdcal==1.4.1',
        'objectpath==0.6.1',
        'html5lib==1.1',
        'shapely==1.8.1.post1',
        'tzwhere==3.0.3',
        'office365-rest-python-client==2.2.1',
        'bs4==0.0.1',
        'beautifulsoup4==4.11.2',
        'patool==1.12',
        'sqlalchemy==1.4.46',
        'tabulate==0.8.7',
        'python-magic==0.4.27',
        'pytomlpp==1.0.11',
        'psutil==5.9.0',
        'networkx==2.8.5',
        'matplotlib==3.5.3',
        'pendulum==2.1.2',
        'psycopg2-binary>=2.9.1',
        'navconfig[default]>=1.1.0',
        'navigator-session>=0.3.3',
        'asyncdb[default]>=2.2.0',
        'async-notify>=0.9.2',
        'navigator-api[locale]>=2.6.4'
    ],
    tests_require=[
            'pytest>=5.4.0',
            'coverage',
            'pytest-asyncio==0.14.0',
            'pytest-xdist==2.1.0',
            'pytest-assume==2.4.2'
    ],
    ext_modules=cythonize(extensions),
    entry_points={
        'console_scripts': [
            'di = flowtask.__main__:main',
            'task = flowtask.__main__:main',
        ]
    },
    project_urls={  # Optional
        'Source': 'https://github.com/phenobarbital/flowtask',
        'Funding': 'https://paypal.me/phenobarbital',
        'Say Thanks!': 'https://saythanks.io/to/phenobarbital',
    },
)
