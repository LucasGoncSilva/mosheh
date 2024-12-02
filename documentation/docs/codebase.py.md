
# File: `codebase.py`
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

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from custom_types import CodebaseDict
    ```

### `#!py import StandardReturn`

Path: `#!py custom_types`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from custom_types import StandardReturn
    ```

### `#!py import handle_def_nodes`

Path: `#!py handlers`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from handlers import handle_def_nodes
    ```

### `#!py import add_to_dict`

Path: `#!py utils`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from utils import add_to_dict
    ```

### `#!py import convert_to_regular_dict`

Path: `#!py utils`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from utils import convert_to_regular_dict
    ```

### `#!py import nested_dict`

Path: `#!py utils`

Category: 3rd Party

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

Type: `#!py ...`

Return Type: `#!py CodebaseDict`

Decorators: `#!py None`

Args: `#!py root: str`

Kwargs: `#!py None`

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
        for file in iterate(root):
            if file.endswith('.py'):
                with open(file, encoding='utf-8') as f:
                    code: str = f.read()
                tree: ast.AST = ast.parse(code, filename=file)
                statements: list[StandardReturn] = []
                for node in ast.walk(tree):
                    data: list[StandardReturn] = handle_def_nodes(node)
                    if data:
                        statements.extend(data)
                add_to_dict(codebase, file.split(sep), statements)
        return convert_to_regular_dict(codebase)
    ```

### `#!py def iterate`

Type: `#!py ...`

Return Type: `#!py Generator[str, Any, Any]`

Decorators: `#!py None`

Args: `#!py root: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def iterate(root: str) -> Generator[str, Any, Any]:
        """
        Iterates through every dir and file starting at provided root.

        Iterates using for-loop in os.walk and for dirpath and file in
        files yields the path for each file from the provided root to it.

        :param root: The root to be used as basedir.
        :type root: str
        :return: The path for each file on for-loop.
        :rtype: Generator[str, Any, Any]
        """
        for (dirpath, _, files) in walk(root):
            for file in files:
                yield path.join(dirpath, file)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
