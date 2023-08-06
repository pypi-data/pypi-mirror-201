# -*- coding: utf-8 -*-
"""Data-Integration Task Runner.

This Module can run data-integration tasks, received parametrized json-tasks
 and return results.

INFO:
 - _args
 - _params are the variables that comes from kwargs (json or key:value)
   * --params="{\"key\": \"value\"}"
 - _attributes root-level attributes of the components
   * --attribute_name=value
 - _stepsattrs: passing attributes only for a Component (only from calling object task)
 - _arguments: are command-line arguments or a list of arguments (if task needed)
 - _variables: are passed between components (or starting)
   * --variables name1:value1 name2:value2 ...
 Support of different kind of params and args:
 --variable1=1 --variable2=2 --args test:hola prueba:mundo chivo:conejo --hola mundo --params="{\"key\": \"value\"}"
 type --variable1=1, --hola mundo and --args test:hola will be passed like args
"""