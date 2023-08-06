# ezstools
Ezstools is a Python library that provides a variety of tools and modules to help developers deal with common issues. Whether you need to manipulate JSON files, generate random data, or interact with the console, ezstools has you covered.

*Disclaimer: This library is still in development and is not yet ready for production use.*

## Installation
```bash
pip install ezstools
```

## Usage
Here's an example of how to use the `convert_num` function from the `funcs` module:
```python
from ezstools.funcs import convert_num

print(convert_num(123456)) # 123K
```
Here's another example, this time using the `string_tools` module:
```python
from ezstools.string_tools import most_similar_string, random_string

print(most_similar_string(
    target="Hello Ezstools",
    options=[
        "Hello Ezstools",
        "Hello world",
        "ezstools",
        "hello",
        random_string(length=10)
    ]
)) 
```


## Modules:

### console_utils
contains methods to interact with the console, including methods to display links and pick menus.

### funcs
provides a collection of general-purpose functions, such as timeit for timing code snippets and convert_num for converting a string to a number.

### json_tools
provides tools to manipulate JSON files, including methods to load and dump JSON data.

### random_generator
provides tools to generate random data, such as random names or email addresses.

### html_slice
The html_slice module provides a command-line interface (CLI) tool to slice HTML files, allowing you to extract or modify 
specific parts of the file.

### string_tools
provides tools for string manipulation, including find and replace operations, normalization, and more.

### custom_iterables
provides a set of methods to make built-in iterables more powerful, such as map, filter, and reduce.

### simple_kv
The simple_kv module provides tools to interact and manipulate simple key-value files (.skv), a custom file format.

### module_tools
provides tools to create and interact with Python modules, such as methods to import and reload modules.

# LICENSE
`ezstools` is licensed under the MIT License. Please see the LICENSE file for more information.