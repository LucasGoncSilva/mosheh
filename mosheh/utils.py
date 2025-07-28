"""
If a func can help and be classified as an "utility function", problably that function
is going to be here.

Functions to be here must be independent, work isolated from other ones and decoupled
away from any external or global logic. They must work just by itself, even if
implementing some functionality which can be related.

Here are usually maintained reusable code applicable everywhere.
"""

import importlib.util
import sysconfig
from bisect import bisect_left
from collections import defaultdict
from collections.abc import Sequence
from typing import Any, cast

from mosheh.constants import BUILTIN_MODULES
from mosheh.types.basic import CodebaseDict, ModuleName, StandardReturn
from mosheh.types.enums import ImportType


def bin(item: Any, universe: Sequence[Any]) -> bool:
    """
    Binary Search algorithm which returns not the index, but a boolean.

    Uses Python's bisect.bisect_left function to efficiently find the insertion point
    of the item in the sorted sequence, then checks if the item exists at that
    position.

    Example:

    ```python
    lst: list[int] = [1, 2, 3, 4, 5]
    num: int = 4
    bin(num, lst)
    # True
    ```

    :param item: The item to check if exists in.
    :type item: Any
    :param universe: The SORTED iterable to be evaluated.
    :type universe: Sequence[Any]
    :return: If the item is found in the universe.
    :rtype: bool
    """

    i = bisect_left(universe, item)
    return i < len(universe) and universe[i] == item


def get_import_type(lib: ModuleName) -> ImportType:
    """
    Classifies the module into a valid `ImportType` alternative.

    By literally just... find spec using... unhh... find_spec()... searches
    for modules in the environment path and returns it.

    Example:

    ```python
    get_import_type('mkdocs')
    # ImportType.TrdParty
    ```

    :param lib: The lib name, e.g. "numpy" or "numba".
    :type lib: ModuleName
    :return: `ImportType` enum for native, 3rd party or local one.
    :rtype: ImportType
    """

    try:
        if lib in BUILTIN_MODULES:
            return ImportType.Native

        spec = importlib.util.find_spec(lib)
        if not spec or not spec.origin:
            return ImportType.Local

        origin: str = spec.origin

        if origin in ('built-in', 'frozen') or (
            origin.endswith(('.so', '.pyd', '.dll')) and 'lib-dynload' in origin
        ):
            return ImportType.Native

        if 'site-packages' in origin or 'dist-packages' in origin:
            return ImportType.TrdParty

        stdlib_path = sysconfig.get_paths()['stdlib']
        if origin.startswith(stdlib_path):
            return ImportType.Native

        return ImportType.Local
    except Exception:
        return ImportType.Local


def nested_defaultdict() -> defaultdict[Any, Any]:
    """
    Creates and returns a nested dictionary using `collections.defaultdict`.

    This function generates a `defaultdict` where each key defaults to another
    `nested_defaultdict`, allowing the creation of arbitrarily deep dictionaries without
    needing to explicitly define each level.

    Key concepts:
    - defaultdict: A specialized dictionary from the `collections` module
      that automatically assigns a default value for missing keys. In this case, the
      default value is another `nested_defaultdict`, enabling recursive dict nesting.

    Example:

    ```python
    d = nested_defaultdict()
    d['level1']['level2']['level3'] = 'text'
    # {'level': {'level2': {'level3': 'text'}}}
    ```

    :return: A `defaultdict` instance configured for recursive nesting.
    :rtype: defaultdict[Any, Any]
    """

    return defaultdict(nested_defaultdict)


def add_to_nested_defaultdict(
    structure: defaultdict[Any, Any],
    path: list[str],
    data: list[StandardReturn],
) -> defaultdict[Any, Any]:
    """
    Adds data to a nested dictionary structure based on a specified path.

    This function traverses a nested dictionary (`structure`) using a list of keys
    (`path`). If the path consists of a single key, the data is added directly to the
    corresponding level. Otherwise, the function recursively traverses deeper into the
    structure, creating nested dictionaries as needed, until the data is added at the
    specified location.

    Key concepts:
    - Recursive Traversal: The function calls itself recursively to traverse and modify
      deeper levels of the nested dictionary.

    Example:

    ```python
    structure: defaultdict = nested_defaultdict()
    path: list[str] = ['level1', 'level2', 'level3']
    data: list[StandardReturn] = [{'key': 'value'}]
    add_to_nested_defaultdict(structure, path, data)
    # defaultdict(defaultdict, {'level1': {'level2': {'level3': [{'key': 'value'}]}}})
    ```

    :param structure: The nested dictionary to modify.
    :type structure: defaultdict[Any, Any]
    :param path: A list of keys representing the path to the target location.
    :type path: list[str]
    :param data: The data to add at the specified path.
    :type data: list[StandardReturn]
    :return: The modified dictionary with the new data added.
    :rtype: defaultdict[Any, Any]
    """

    if len(path) == 1:
        structure[path[0]] = data
    elif len(path) > 1:
        structure[path[0]] = add_to_nested_defaultdict(
            structure[path[0]], path[1:], data
        )

    return structure


def build_nav_struct(
    tree: CodebaseDict, codebase_nav_path: str = 'Codebase', prefix: str = ''
) -> list[dict[str, Any]]:
    """
    Processes the `codebase.read_codebase` into valid yaml "Nav" dump format.

    While taking the codebase structure, processed by `codebase.read_codebase` on the
    `Codebase` format, recursively iterates the codebase mapping every file and
    directory, returning something similar to the example below:

    ```python
    [
        {
            'PROJECT': [
                {'manage.py': 'Codebase/PROJECT/manage.py.md'},
                {
                    'dummy': [
                        {'tests.py': 'Codebase/PROJECT/dummy/tests.py.md'},
                        {'admin.py': 'Codebase/PROJECT/dummy/admin.py.md'},
                        {'apps.py': 'Codebase/PROJECT/dummy/apps.py.md'},
                        {'models.py': 'Codebase/PROJECT/dummy/models.py.md'},
                        {'urls.py': 'Codebase/PROJECT/dummy/urls.py.md'},
                        {'__init__.py': 'Codebase/PROJECT/dummy/__init__.py.md'},
                        {'views.py': 'Codebase/PROJECT/dummy/views.py.md'},
                    ]
                },
                {
                    'CORE': [
                        {'wsgi.py': 'Codebase/PROJECT/CORE/wsgi.py.md'},
                        {'asgi.py': 'Codebase/PROJECT/CORE/asgi.py.md'},
                        {'urls.py': 'Codebase/PROJECT/CORE/urls.py.md'},
                        {'settings.py': 'Codebase/PROJECT/CORE/settings.py.md'},
                        {'__init__.py': 'Codebase/PROJECT/CORE/__init__.py.md'},
                    ]
                },
            ]
        }
    ]
    ```

    The directories has a list as key-value pair, while files has their markdown
    equivalent path for their markdown documented result.

    :param tree: Codebase `codebase.read_codebase` struct.
    :type tree: Codebase
    :param codebase_nav_path: Expected codebase nav name to be used/found.
    :type codebase_nav_path: str = 'Codebase'
    :param prefix: Accumulative string path for concat.
    :type tree: str = ''
    :return: Formatted "yaml-nav-dumpable" codebase structure.
    :rtype: list[dict[str, Any]]
    """

    result: list[dict[str, Any]] = []

    for name, content in cast(dict[str, Any], tree).items():
        full_path = f'{prefix}/{name}' if prefix else name

        if isinstance(content, list):
            result.append({name: f'{codebase_nav_path}/{full_path}.md'})
        else:
            nested: list[dict[str, Any]] = build_nav_struct(
                content, codebase_nav_path, full_path
            )
            result.append({name: nested})

    return result


def convert_to_regular_dict(d: defaultdict[Any, Any] | dict[Any, Any]) -> CodebaseDict:
    """
    Converts a nested `defaultdict` into a regular dictionary.

    This function recursively traverses a `defaultdict` and its nested dictionaries,
    converting all instances of `defaultdict` into standard Python dictionaries. This
    ensures the resulting structure is free of `defaultdict` behavior.

    Key concepts:
    - defaultdict: A dictionary subclass from the `collections` module that provides
      default values for missing keys. This func removes that behavior by converting
      it into a regular dictionary.
    - Recursive Conversion: The function traverses and converts all nested dict,
      ensuring the entire structure is converted.

    Example:

    ```python
    d: defaultdict = nested_defaultdict()
    d['level1']['level2'] = 'value'
    convert_to_regular_dict(d)
    # {'level1': {'level2': 'value'}}
    ```

    :param d: The dictionary to convert. Can include nested `defaultdict` instances.
    :type d: defaultdict[Any, Any] | dict[Any, Any]
    :return: A dict where all `defaultdict` instances are converted to regular dicts.
    :rtype: CodebaseDict
    """

    if isinstance(d, defaultdict):
        d = {k: convert_to_regular_dict(v) for k, v in d.items()}

    return d


def standard_struct() -> StandardReturn:
    """
    Defines the standard keys and values of code data dict.

    The keys are listed below, followed by they types, as below:

    ```python
    dct: StandardReturn = {
        'statement': Statement,
        'name': Token,
        'tokens': list[Token | ImportedIdentifier],
        'annot': Annotation,
        'value': Value,
        'decorators': list[Decorator],
        'inheritance': list[Inheritance],
        'path': ModulePath,
        'category': ImportType | FunctionType,
        'docstring': Docstring | None,
        'rtype': Annotation,
        'args': Arg,
        'kwargs': Kwarg,
        'test': AssertionTest,
        'msg': AssertionMessage,
        'code': CodeSnippet,
    }
    ```
    Any other datatype different from those above must be avoided as much as possible
    to maintain the codebase at the same struct. Python is not the best when talking
    about types like Java or Rust, so keep this in mind is really necessary.

    Example:

    ```python
    standard_struct()
    # {}
    ```

    :return: An empty dict annotated with special custom type.
    :rtype: StandardReturn
    """

    return {}


def indent_code(code: str, level: int = 4) -> str:
    """
    Used just for applying indentation to code before building the doc `.md` file.

    By receiving the code itself and an indentation number, defaulting to 4, and for
    each line applies the desired indentation level, A.K.A leftpad.

    Example:

    ```python
    code: str = \"\"\"for i in range(10):\n        str(i)\"\"\"
    level: int = 4
    code
    # for i in range(10):\n#     str(i)
    indent_code(code, level)
    #     for i in range(10):\n#         str(i)
    ```

    :param code: The code snippet to be formatted.
    :type code: str
    :param level: The number of spaces to leftpad each line.
    :type level: int = 4
    :return: The code snippet leftpadded.
    :rtype: str
    """

    indent: str = ' ' * level
    new_code: str = '\n'.join(
        map(lambda line: f'{indent}{line}' if line.strip() else '', code.splitlines())
    )

    return new_code


def remove_abspath_from_codebase(
    d: CodebaseDict,
) -> CodebaseDict:
    """
    Removes abspath dirs names from `CodebaseDict` structure.

    Because of typing annotation stuff, this function just invokes the sibling with
    almost the same name, which is recursive, to handle the codebase-generated dict
    and remove any path outside the codebase but present due `os.path.abspath` calls.

    The output is exactly the same `CodebaseDict` but with no abspath dir present.

    :param d: `codebase.read_codebase` output structure.
    :type d: CodebaseDict
    :return: `codebase.read_codebase` output removing abspath.
    :rtype: CodebaseDict
    """

    return _remove_abspath_from_codebase_helper(next(iter(d.values())))


def _remove_abspath_from_codebase_helper(
    d: CodebaseDict | list[StandardReturn],
) -> CodebaseDict:
    """
    ### YOU SHOULD NOT BE CALLING THIS FUNCTION!

    Removes abspath dirs names from `CodebaseDict` structure.

    The real recursive abspath-remove-o-matic function, not used primary just because
    of typing annotations.

    Inside it, recursively iterates the income `d`, goes until the first non-dictionary
    or single-length item is found, returning from this point.

    :param d: `codebase.read_codebase` output structure.
    :type d: CodebaseDict | list[StandardReturn]
    :return: `codebase.read_codebase` output removing abspath.
    :rtype: CodebaseDict
    """

    if isinstance(d, dict):
        deeper = next(iter(d.values()))

        if isinstance(deeper, dict) and len(deeper) == 1:
            return _remove_abspath_from_codebase_helper(deeper)

    return cast(CodebaseDict, d)
