# File: `codebase.py`

Role: Python Source Code

Path: `mosheh`

---

## Imports

### `#!py import ast`

Path: `#!py None`

Category: Native

??? example "SNIPPET"

    ```py
    import ast
    ```

### `#!py import Generator`

Path: `#!py collections.abc`

Category: Native

??? example "SNIPPET"

    ```py
    from collections.abc import Generator
    ```

### `#!py import Logger`

Path: `#!py logging`

Category: Native

??? example "SNIPPET"

    ```py
    from logging import Logger
    ```

### `#!py import getLogger`

Path: `#!py logging`

Category: Native

??? example "SNIPPET"

    ```py
    from logging import getLogger
    ```

### `#!py import path`

Path: `#!py os`

Category: Native

??? example "SNIPPET"

    ```py
    from os import path
    ```

### `#!py import sep`

Path: `#!py os`

Category: Native

??? example "SNIPPET"

    ```py
    from os import sep
    ```

### `#!py import walk`

Path: `#!py os`

Category: Native

??? example "SNIPPET"

    ```py
    from os import walk
    ```

### `#!py import Any`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Any
    ```

### `#!py import CodebaseDict`

Path: `#!py custom_types`

Category: Local

??? example "SNIPPET"

    ```py
    from custom_types import CodebaseDict
    ```

### `#!py import FileRole`

Path: `#!py custom_types`

Category: Local

??? example "SNIPPET"

    ```py
    from custom_types import FileRole
    ```

### `#!py import StandardReturn`

Path: `#!py custom_types`

Category: Local

??? example "SNIPPET"

    ```py
    from custom_types import StandardReturn
    ```

### `#!py import handle_def_nodes`

Path: `#!py handler`

Category: Local

??? example "SNIPPET"

    ```py
    from handler import handle_def_nodes
    ```

### `#!py import add_to_dict`

Path: `#!py utils`

Category: Local

??? example "SNIPPET"

    ```py
    from utils import add_to_dict
    ```

### `#!py import convert_to_regular_dict`

Path: `#!py utils`

Category: Local

??? example "SNIPPET"

    ```py
    from utils import convert_to_regular_dict
    ```

### `#!py import nested_dict`

Path: `#!py utils`

Category: Local

??? example "SNIPPET"

    ```py
    from utils import nested_dict
    ```

---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def read_codebase`

Type: `#!py Function`

Return Type: `#!py CodebaseDict`

Decorators: `#!py None`

Args: `#!py root: str`

Kwargs: `#!py None`

Iterates through the codebase and collects all info needed.

Using `iterate()` to navigate and `handle_def_nodes()` to get data,
stores the collected data in a dict of type CodebaseDict, defined
in constants.py file.

Also works as a dispatch-like, matching the files extensions,
leading each file to its flow.

:param root: The root path/dir to be iterated.

:type root: str

:return: All the codebase data collected.

:rtype: CodebaseDict

??? example "SNIPPET"

    ```py
    def read_codebase(root: str) -> CodebaseDict:
        """
        Iterates through the codebase and collects all info needed.

        Using `iterate()` to navigate and `handle_def_nodes()` to get data,
        stores the collected data in a dict of type CodebaseDict, defined
        in constants.py file.

        Also works as a dispatch-like, matching the files extensions,
        leading each file to its flow.

        :param root: The root path/dir to be iterated.
        :type root: str
        :return: All the codebase data collected.
        :rtype: CodebaseDict
        """
        codebase: CodebaseDict = nested_dict()
        logger.info(f'Starting iteration through {root}')
        for file in _iterate(root):
            logger.debug(f'Iterating: {file}')
            if file.endswith('.py'):
                logger.debug(f'.py: {file}')
                with open(file, encoding='utf-8') as f:
                    code: str = f.read()
                    logger.debug(f'{file} read')
                tree: ast.AST = ast.parse(code, filename=file)
                logger.debug('Code tree parsed')
                statements: list[StandardReturn] = []
                for node in ast.walk(tree):
                    logger.debug(f'Node: {type(node)}')
                    if isinstance(node, ast.ClassDef):
                        _mark_methods(node)
                    elif isinstance(node, ast.FunctionDef) and getattr(node, 'parent', None):
                        continue
                    data: list[StandardReturn] = handle_def_nodes(node)
                    logger.debug('Node processed')
                    if data:
                        statements.extend(data)
                        logger.debug('Node inserted into statement list')
                statements.insert(0, {'__role__': FileRole.PythonSourceCode})
                add_to_dict(codebase, file.split(sep), statements)
                logger.debug(f'{file} stmts added to CodebaseDict')
        return convert_to_regular_dict(codebase)
    ```

### `#!py def _mark_methods`

Type: `#!py Function`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py node: ast.ClassDef`

Kwargs: `#!py None`

Marks all `FunctionDef` nodes within a given `ClassDef` node by setting a
`parent` attribute to indicate their association with the class.

This function iterates over the child nodes of the provided class node, and
for each method (a `FunctionDef`), it assigns the class type (`ast.ClassDef`)
to the `parent` attribute of the method node.

:param node: The class definition node containing methods to be marked.

:type node: ast.ClassDef

:return: No data to be returned

:rtype: None

??? example "SNIPPET"

    ```py
    def _mark_methods(node: ast.ClassDef) -> None:
        """
        Marks all `FunctionDef` nodes within a given `ClassDef` node by setting a
        `parent` attribute to indicate their association with the class.

        This function iterates over the child nodes of the provided class node, and
        for each method (a `FunctionDef`), it assigns the class type (`ast.ClassDef`)
        to the `parent` attribute of the method node.

        :param node: The class definition node containing methods to be marked.
        :type node: ast.ClassDef
        :return: No data to be returned
        :rtype: None
        """
        for child_node in ast.iter_child_nodes(node):
            if isinstance(child_node, ast.FunctionDef):
                setattr(child_node, 'parent', ast.ClassDef)
    ```

### `#!py def encapsulated_mark_methods_for_unittest`

Type: `#!py Function`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py node: ast.ClassDef`

Kwargs: `#!py None`

Just encapsulates `_mark_methods` function to external use, only for unittesting.

:param node: The class definition node containing methods to be marked.

:type node: ast.ClassDef

:return: No data to be returned

:rtype: None

??? example "SNIPPET"

    ```py
    def encapsulated_mark_methods_for_unittest(node: ast.ClassDef) -> None:
        """
        Just encapsulates `_mark_methods` function to external use, only for unittesting.

        :param node: The class definition node containing methods to be marked.
        :type node: ast.ClassDef
        :return: No data to be returned
        :rtype: None
        """
        _mark_methods(node)
    ```

### `#!py def _iterate`

Type: `#!py Generator`

Return Type: `#!py Generator[str, Any, Any]`

Decorators: `#!py None`

Args: `#!py root: str`

Kwargs: `#!py None`

Iterates through every dir and file starting at provided root.

Iterates using for-loop in os.walk and for dirpath and file in
files yields the path for each file from the provided root to it.

:param root: The root to be used as basedir.

:type root: str

:return: The path for each file on for-loop.

:rtype: Generator[str, Any, Any]

??? example "SNIPPET"

    ```py
    def _iterate(root: str) -> Generator[str, Any, Any]:
        """
        Iterates through every dir and file starting at provided root.

        Iterates using for-loop in os.walk and for dirpath and file in
        files yields the path for each file from the provided root to it.

        :param root: The root to be used as basedir.
        :type root: str
        :return: The path for each file on for-loop.
        :rtype: Generator[str, Any, Any]
        """
        for dirpath, _, files in walk(root):
            for file in files:
                yield path.join(dirpath, file)
    ```

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
