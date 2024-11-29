import ast
from typing import Final, cast

import constants
from custom_types import (
    ArgsKwargs,
    ImportType,
    StandardReturn,
    StandardReturnProccessor,
    Statement,
)
from utils import bin, is_lib_installed, standard_struct


def handle_def_nodes(node: ast.AST) -> StandardReturn:
    """
    Processes an abstract syntax tree (AST) node and returns a handler for the node.

    This function analyzes a given `ast.AST` node, determines its type, and processes
    it using the appropriate handler function. It supports a variety of node types such
    as imports, constants, functions, classes, and assertions, delegating the handling
    to specialized functions for each case.

    The function categorizes and handles nodes as follows:
    - Imports: `ast.Import | ast.ImportFrom`
    - Constants: `ast.Assign | ast.AnnAssign`
    - Functions: `ast.FunctionDef | ast.AsyncFunctionDef`
    - Classes: `ast.ClassDef`
    - Assertions: `ast.Assert`

    :param node: the AST node to process
    :type node: ast.AST
    :return: an object containing information associated with the node
    :rtype: StandardReturn
    """

    data: StandardReturn = {}

    # -------------------------
    # Imports - ast.Import | ast.ImportFrom
    # -------------------------

    if isinstance(node, ast.Import):
        data = handle_import(data, node)
    elif isinstance(node, ast.ImportFrom):
        data = handle_import_from(data, node)

    # -------------------------
    # Constants - ast.Assign | ast.AnnAssign
    # -------------------------

    elif isinstance(node, ast.Assign):
        lst: list[str] = []
        for i in node.targets:
            lst.append(cast(str, handle_node(i)))

        if any(map(str.isupper, lst)) or any(
            map(lambda x: x in constants.ACCEPTABLE_LOWER_CONSTANTS, lst)
        ):
            data = handle_assign(data, node)
    elif isinstance(node, ast.AnnAssign):
        if isinstance(node.target, ast.Name) and node.target.id.isupper():
            data = handle_annassign(data, node)

    # -------------------------
    # Functions - ast.FunctionDef | ast.AsyncFunctionDef
    # -------------------------

    elif isinstance(node, ast.FunctionDef):
        data = handle_function_def(data, node)
    elif isinstance(node, ast.AsyncFunctionDef):
        data = handle_async_function_def(data, node)

    # -------------------------
    # Classes - ast.ClassDef
    # -------------------------

    elif isinstance(node, ast.ClassDef):
        data = handle_class_def(data, node)

    # -------------------------
    # Assertions - ast.Assert
    # -------------------------

    elif isinstance(node, ast.Assert):
        data = handle_assert(data, node)

    return data


def handle_node(node: ast.AST | ast.expr | None) -> StandardReturnProccessor | None:
    """
    The same of `handle_def_nodes()`, but extended to attend contemplate more nodes.

    Extended nodes contemplated are:
    - Calls - `ast.Call`
    - Constants - `ast.Constant`
    - Attributes - `ast.Attribute`
    - Lists - `ast.List`
    - Tuples - `ast.Tuple`
    - Sets - `ast.Set`
    - Dicts - `ast.Dict`
    - BinOps - `ast.BinOp`
    - Subscripts - `ast.Subscript`
    - Slices - `ast.Slice`
    - Names - `ast.Name`

    :param node: the AST node to process
    :type node: ast.AST | ast.expr | None
    :return: an object containing information associated with the node or None
    :rtype: StandardReturnProccessor | None
    """

    if node is None:
        return node

    data: StandardReturnProccessor = {}

    # -------------------------
    # Imports - ast.Import | ast.ImportFrom
    # -------------------------

    if isinstance(node, ast.Import):
        data = handle_import(data, node)
    elif isinstance(node, ast.ImportFrom):
        data = handle_import_from(data, node)

    # -------------------------
    # Constants - ast.Assign | ast.AnnAssign
    # -------------------------

    elif isinstance(node, ast.Assign):
        lst: list[str] = [
            handle_constant(i) for i in node.targets if isinstance(i, ast.Constant)
        ]
        if any(map(str.isupper, lst)):
            data = handle_assign(data, node)
    elif isinstance(node, ast.AnnAssign):
        if isinstance(node.target, ast.Name) and node.target.id.isupper():
            data = handle_annassign(data, node)

    # -------------------------
    # Functions - ast.FunctionDef | ast.AsyncFunctionDef
    # -------------------------

    elif isinstance(node, ast.FunctionDef):
        data = handle_function_def(data, node)
    elif isinstance(node, ast.AsyncFunctionDef):
        data = handle_async_function_def(data, node)

    # -------------------------
    # Classes - ast.ClassDef
    # -------------------------

    elif isinstance(node, ast.ClassDef):
        data = handle_class_def(data, node)

    # -------------------------
    # Assertions - ast.Assert
    # -------------------------

    elif isinstance(node, ast.Assert):
        data = handle_assert(data, node)

    # -------------------------
    # Calls - ast.Call
    # -------------------------

    elif isinstance(node, ast.Call):
        data = handle_call(node)

    # -------------------------
    # Literals - ast.Constants
    # -------------------------

    elif isinstance(node, ast.Constant):
        data = handle_constant(node)

    # -------------------------
    # Attributes - ast.Attribute
    # -------------------------

    elif isinstance(node, ast.Attribute):
        data = handle_attribute(node)

    # -------------------------
    # Lists - ast.List
    # -------------------------

    elif isinstance(node, ast.List):
        data = handle_list(node)

    # -------------------------
    # Tuples - ast.Tuple
    # -------------------------

    elif isinstance(node, ast.Tuple):
        data = handle_tuple(node)

    # -------------------------
    # Sets - ast.Set
    # -------------------------

    elif isinstance(node, ast.Set):
        data = handle_set(node)

    # -------------------------
    # Dicts - ast.Dict
    # -------------------------

    elif isinstance(node, ast.Dict):
        data = handle_dict(node)

    # -------------------------
    # Basic Operations - "+", "-", "*", "/", ...
    # -------------------------

    elif isinstance(node, ast.BinOp):
        data = handle_binop(node)

    # -------------------------
    # SubScripts - ast.Subscript
    # -------------------------

    elif isinstance(node, ast.Subscript):
        data = handle_subscript(node)

    # -------------------------
    # Slices - ast.Slice
    # -------------------------

    elif isinstance(node, ast.Slice):
        data = handle_slice(node)

    # -------------------------
    # Names - ast.Name
    # -------------------------

    elif isinstance(node, ast.Name):
        data = handle_name(node)

    # -------------------------
    # Names - ast.Compare
    # -------------------------

    elif isinstance(node, ast.Compare):
        data = handle_compare(node)

    return data


def __handle_import(lib_name: str) -> StandardReturn:
    """
    Constructs a standardized dictionary representation for an import statement.

    This function processes the given library name, determines its import category
    (local, native, or third-party), and builds a standardized dictionary structure
    representing the import statement. The resulting data includes information about
    the statement type, library name, import category, and the generated import code.

    Key concepts:
    - Import Categorization: Determines whether the library is native (built-in),
      third-party, or local.
    - Standardized Structure: Returns a dictionary conforming to the `StandardReturn`
      format, ensuring consistency across codebase documentation.
    - Dynamic Code Generation: Constructs the import statement dynamically based on
      the library name.

    Example:
    ```python
    data: StandardReturn = __handle_import('os')
    data
    # {
    #     'statement': Statement.Import,
    #     'name': 'os',
    #     'path': None,
    #     'category': ImportType.Native,
    #     'code': 'import os',
    # }
    ```

    :param lib_name: the name of the library to be imported
    :type lib_name: str
    :return: a standardized dictionary representing the import statement
    :rtype: StandardReturn
    """

    statement: Statement = Statement.Import
    path: Final[None] = None
    category: ImportType = ImportType.Local

    if bin(lib_name, constants.BUILTIN_MODULES):
        category = ImportType.Native
    elif is_lib_installed(lib_name):
        category = ImportType.TrdParty

    data: StandardReturn = standard_struct()

    data.update(
        {
            'statement': statement,
            'name': lib_name,
            'path': path,
            'category': category,
            'code': f'import {lib_name}',
        }
    )

    return data


def handle_import(struct: StandardReturn, node: ast.Import) -> StandardReturn:
    """
    Updates a standardized structure with information from an import statement node.

    This function processes an AST import node, extracts the library names being
    imported, and updates the given `StandardReturn` structure with details about
    each library. It leverages the `__handle_import` function to standardize the data
    for each imported library.

    Key concepts:
    - AST Parsing: Processes Python's AST nodes for import statements.
    - Data Standardization: Utilizes `__handle_import` to format each import into a
      consistent structure.
    - Structure Update: Modifies the provided `struct` in-place with import data.

    Example:
    ```python
    struct = standard_struct()
    node = ast.parse('import os, sys').body[0]
    updated_struct = handle_import(struct, node)
    updated_struct
    # Outputs standardized data for 'os' and 'sys' imports.
    ```

    :param struct: the structure to be updated with import details
    :type struct: StandardReturn
    :param node: the AST node representing an import statement
    :type node: ast.Import
    :return: the updated structure with information about the imported libraries
    :rtype: StandardReturn
    """

    for lib in [i.name for i in node.names]:
        struct.update(__handle_import(lib))

    # BUG: returns only last element -> change to list and return list struct
    return struct


def handle_import_from(struct: StandardReturn, node: ast.ImportFrom) -> StandardReturn:
    """
    Processes an `ast.ImportFrom` node and returnes its data.

    This function iterates over the imported module names within an `ast.ImportFrom`
    node, classifying each module into one of the following categorys, as
    `handle_import`:
    - Native: The module is a built-in Python module.
    - Third-Party: The module is installed via external libraries.
    - Local: The module is neither built-in nor a third-party library, problably local.

    Each module's data includes its path and category, stored in a structured dict.

    :param node: the AST node representing an import statement
    :type node: ast.ImportFrom
    :return: a dict containing the statement type and categorized module information
    :rtype: StandardReturn
    """

    statement: Final[Statement] = Statement.ImportFrom
    names: Final[list[str]] = [i.name for i in node.names]
    path: Final[str | None] = node.module
    category: ImportType = ImportType.Local
    code: Final[str] = ast.unparse(node)

    mod: str = f'{node.module}'

    if bin(
        f'{mod}.'.split('.')[0],
        constants.BUILTIN_MODULES,
    ):
        category = ImportType.Native
    elif is_lib_installed(mod):
        category = ImportType.TrdParty

    data: StandardReturn = standard_struct()

    for i in names:
        data.update(
            {
                'statement': statement,
                'name': i,
                'path': path,
                'category': category,
                'code': code,
            }
        )

    struct.update(data)

    return struct


def handle_attribute(node: ast.Attribute) -> str:
    """
    Recieves an `ast.Attribute` node and returns its code-like representation as str.

    :param node: the AST node representing a slice expression
    :type node: ast.Attribute
    :return: the readable code-like node build up
    :rtype: str
    """

    return ast.unparse(node)


def handle_call(node: ast.Call) -> str:
    """
    Recieves an `ast.Call` node and returns its code-like representation as str.

    :param node: the AST node representing a slice expression
    :type node: ast.Call
    :return: the readable code-like node build up
    :rtype: str
    """

    return ast.unparse(node)


def handle_constant(node: ast.Constant) -> str:
    """
    Recieves an `ast.Constant` node and returns its code-like representation as str.

    :param node: the AST node representing a slice expression
    :type node: ast.Constant
    :return: the readable code-like node build up
    :rtype: str
    """

    return ast.unparse(node)


def handle_assign(struct: StandardReturn, node: ast.Assign) -> StandardReturn:
    """
    Processes an `ast.Assign` node and returns its data.

    This function analyzes the components of an assignment, including the target vars
    and the assigned value, returning a structured dict with the extracted details.

    Key elements of the returned data:
    - tokens: A list of string repr for all target variables in the assignment.
    - value: A string repr of the value being assigned.

    :param node: the AST node representing an assignment statement
    :type node: ast.Assign
    :return: a dict containing the statement type, target variables, and assigned value
    :rtype: StandardReturn
    """

    statement: Final[Statement] = Statement.Assign
    tokens: Final[list[str]] = [cast(str, handle_node(i)) for i in node.targets]
    value: Final[str] = cast(str, handle_node(node.value))
    code: Final[str] = ast.unparse(node)

    data: StandardReturn = standard_struct()

    data.update(
        {
            'statement': statement,
            'tokens': tokens,
            'value': value,
            'code': code,
        }
    )

    struct.update(data)

    return struct


def handle_binop(node: ast.BinOp) -> str:
    """
    Recieves an `ast.BinOp` node and returns its code-like representation as str.

    :param node: the AST node representing a binary operation expression
    :type node: ast.BinOp
    :return: the readable code-like node build up
    :rtype: str
    """

    return ast.unparse(node)


def handle_annassign(struct: StandardReturn, node: ast.AnnAssign) -> StandardReturn:
    """
    Processes an `ast.AnnAssign` node and returns its data.

    This function analyzes the components of an assignment, including the target var
    and the assigned value, plus the typing notation, returning a structured dict with
    the extracted details.

    Key elements of the returned data:
    - token: A string repr for the target var in the assignment.
    - value: A string repr of the value being assigned.
    - annot: The type hint for the assignment.

    :param node: the AST node representing an assignment statement
    :type node: ast.AnnAssign
    :return: a dict with the statement type, target var, type hint and assigned value
    :rtype: StandardReturn
    """

    statement: Statement = Statement.AnnAssign
    token: str = cast(str, handle_node(node.target))
    annot: str = cast(str, handle_node(node.annotation))
    value: str = ''
    code: str = ast.unparse(node)

    if node.value is not None:
        value = cast(str, handle_node(node.value))

    data: StandardReturn = standard_struct()

    data.update(
        {
            'statement': statement,
            'token': token,
            'annot': annot,
            'value': value,
            'code': code,
        }
    )

    struct.update()

    return struct


def handle_function_def(
    struct: StandardReturn, node: ast.FunctionDef
) -> StandardReturn:
    """
    Processes an `ast.FunctionDef` node and returns its data.

    This function analyzes the components of a func def, mapping the name, decorators,
    arguments (name, type, default value), return type and even the type of function it
    is:
    - Function: a base function, simply defined using `def` keyword;
    - Method: also base function, but defined inside a class (e.g. `def __init__():`);
    - Generator: process an iterable object at a time, on demand, with `yield` inside.

    :param node: the AST node representing a func def statement
    :type node: ast.FunctionDef
    :return: a dict containing the statement type and the data listed before
    :rtype: StandardReturn
    """

    statement: Final[Statement] = Statement.FunctionDef
    name: Final[str] = node.name
    decos: Final[list[str]] = [cast(str, handle_node(i)) for i in node.decorator_list]
    rtype: Final[str] | None = (
        cast(str, handle_node(node.returns)) if node.returns is not None else None
    )
    code: Final[str] = ast.unparse(node)

    arg_lst: ArgsKwargs = []
    s_args: tuple[str | None, str | None, None] | None = None
    kwarg_lst: ArgsKwargs = []
    ss_kwargs: tuple[str | None, str | None, None] | None = None

    has_star_args: bool = True if node.args.vararg is not None else False
    has_star_star_kwargs: bool = True if node.args.kwarg is not None else False

    # Args Logic - Validates `*arg`-like
    if has_star_args and node.args.vararg is not None:
        arg_name: str = f'*{node.args.vararg.arg}'
        annot: str | None = None

        if node.args.vararg.annotation is not None:
            annot = cast(str, handle_node(node.args.vararg.annotation))

        s_args = (arg_name, annot, None)

    default_diff = len(node.args.args) - len(node.args.defaults)

    for i, arg in enumerate(node.args.args, start=1):
        arg_name: str = arg.arg
        annot: str | None = None
        default: str | None = None

        if arg.annotation is not None:
            annot = cast(str, handle_node(arg.annotation))

        if len(node.args.defaults) and default_diff and i > default_diff:
            expected = node.args.defaults[i - 1 - default_diff]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)
        elif len(node.args.defaults) and not (default_diff or i > default_diff):
            expected = node.args.defaults[i - 1]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)

        arg_lst.append((arg_name, annot, default))

    if has_star_args and s_args is not None:
        arg_lst.insert(len(arg_lst), s_args)

    # Kwargs Logic - Validates `**kwarg`-like
    if has_star_star_kwargs and node.args.kwarg is not None:
        arg_name: str = f'*{node.args.kwarg.arg}'
        annot: str | None = None

        if node.args.kwarg.annotation is not None:
            annot = cast(str, handle_node(node.args.kwarg.annotation))

        ss_kwargs = (arg_name, annot, None)

    kwdefault_diff = len(node.args.kwonlyargs) - len(node.args.kw_defaults)

    for i, arg in enumerate(node.args.kwonlyargs, start=1):
        arg_name: str = arg.arg
        annot: str | None = (
            cast(str, handle_node(arg.annotation))
            if arg.annotation is not None
            else None
        )
        default: str | None = None

        if len(node.args.kw_defaults) and (kwdefault_diff and i > kwdefault_diff):
            expected = node.args.kw_defaults[i - 1 - kwdefault_diff]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)
        elif len(node.args.kw_defaults) and not (kwdefault_diff or i > kwdefault_diff):
            expected = node.args.kw_defaults[i - 1]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)

        kwarg_lst.append((arg_name, annot, default))

    if has_star_star_kwargs and ss_kwargs is not None:
        kwarg_lst.insert(len(kwarg_lst), ss_kwargs)

    data: StandardReturn = standard_struct()

    data.update(
        {
            'statement': statement,
            'name': name,
            'decorators': decos,
            'rtype': rtype,
            'args': arg_lst,
            'kwargs': kwarg_lst,
            'code': code,
        }
    )

    struct.update(data)

    return struct


def handle_async_function_def(
    struct: StandardReturn,
    node: ast.AsyncFunctionDef,
) -> StandardReturn:
    """
    Processes an `ast.AsyncFunctionDef` node and returns its data.

    This function analyzes the components of a func def, mapping the name, decorators,
    arguments (name, type, default value), return type and even the type of function it
    is, which in this case can be only one:
    - Coroutine: an async func, defined with `async def` syntax.

    :param node: the AST node representing a func def statement
    :type node: ast.AsyncFunctionDef
    :return: a dict containing the statement type and the data listed before
    :rtype: StandardReturn
    """

    statement: Final[Statement] = Statement.AsyncFunctionDef
    name: Final[str] = node.name
    decos: Final[list[str]] = [cast(str, handle_node(i)) for i in node.decorator_list]
    rtype: Final[str] | None = (
        cast(str, handle_node(node.returns)) if node.returns is not None else None
    )
    code: Final[str] = ast.unparse(node)

    arg_lst: ArgsKwargs = []
    s_args: tuple[str | None, str | None, None] | None = None
    kwarg_lst: ArgsKwargs = []
    ss_kwargs: tuple[str | None, str | None, None] | None = None

    has_star_args: bool = True if node.args.vararg is not None else False
    has_star_star_kwargs: bool = True if node.args.kwarg is not None else False

    # Args Logic - Validates `*arg`-like
    if has_star_args and node.args.vararg is not None:
        arg_name: str = f'*{node.args.vararg.arg}'
        annot: str | None = None

        if node.args.vararg.annotation is not None:
            annot = cast(str, handle_node(node.args.vararg.annotation))

        s_args = (arg_name, annot, None)

    default_diff = len(node.args.args) - len(node.args.defaults)

    for i, arg in enumerate(node.args.args, start=1):
        arg_name: str = arg.arg
        annot: str | None = None
        default: str | None = None

        if arg.annotation is not None:
            annot = cast(str, handle_node(arg.annotation))

        if len(node.args.defaults) and default_diff and i > default_diff:
            expected = node.args.defaults[i - 1 - default_diff]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)
        elif len(node.args.defaults) and not (default_diff or i > default_diff):
            expected = node.args.defaults[i - 1]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)

        arg_lst.append((arg_name, annot, default))

    if has_star_args and s_args is not None:
        arg_lst.insert(len(arg_lst), s_args)

    # Kwargs Logic - Validates `**kwarg`-like
    if has_star_star_kwargs and node.args.kwarg is not None:
        arg_name: str = f'*{node.args.kwarg.arg}'
        annot: str | None = None

        if node.args.kwarg.annotation is not None:
            annot = cast(str, handle_node(node.args.kwarg.annotation))

        ss_kwargs = (arg_name, annot, None)

    kwdefault_diff = len(node.args.kwonlyargs) - len(node.args.kw_defaults)

    for i, arg in enumerate(node.args.kwonlyargs, start=1):
        arg_name: str = arg.arg
        annot: str | None = (
            cast(str, handle_node(arg.annotation))
            if arg.annotation is not None
            else None
        )
        default: str | None = None

        if len(node.args.kw_defaults) and (kwdefault_diff and i > kwdefault_diff):
            expected = node.args.kw_defaults[i - 1 - kwdefault_diff]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)
        elif len(node.args.kw_defaults) and not (kwdefault_diff or i > kwdefault_diff):
            expected = node.args.kw_defaults[i - 1]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)

        kwarg_lst.append((arg_name, annot, default))

    if has_star_star_kwargs and ss_kwargs is not None:
        kwarg_lst.insert(len(kwarg_lst), ss_kwargs)

    data: StandardReturn = standard_struct()

    data.update(
        {
            'statement': statement,
            'name': name,
            'decorators': decos,
            'rtype': rtype,
            'args': arg_lst,
            'kwargs': kwarg_lst,
            'code': code,
        }
    )

    struct.update(data)

    return struct


def handle_class_def(struct: StandardReturn, node: ast.ClassDef) -> StandardReturn:
    """
    Processes an `ast.ClassDef` node and returns its data.

    This function analyzes the components of a class definition, including its name,
    base classes, decorators, and keyword arguments, returning a structured dict with
    the extracted details.

    Key elements of the returned data:
    - name: The name of the class as a string;
    - parents: A list of string reprs for the base classes of the class;
    - decos: A list of string reprs for all decorators applied to the class;
    - kwargs: A list of tuples, in `(name, value)` style.

    :param node: the AST node representing a class definition
    :type node: ast.ClassDef
    :return: a dict with the statement type, name, base classes, decorators, and kwargs
    :rtype: StandardReturn
    """

    statement: Final[Statement] = Statement.ClassDef
    name: Final[str] = node.name
    inheritance: Final[list[str]] = [
        cast(str, handle_node(i)) for i in node.bases if isinstance(i, ast.Name)
    ]
    decos: Final[list[str]] = [cast(str, handle_node(i)) for i in node.decorator_list]
    kwargs: ArgsKwargs = cast(
        ArgsKwargs, [(i.arg, None, i.value) for i in node.keywords]
    )
    code: Final[str] = ast.unparse(node)

    data: StandardReturn = standard_struct()

    data.update(
        {
            'statement': statement,
            'name': name,
            'inheritance': inheritance,
            'decorators': decos,
            'kwargs': kwargs,
            'code': code,
        }
    )

    struct.update(data)

    return struct


def handle_compare(node: ast.Compare) -> str:
    """
    Recieves an `ast.Compare` node and returns its code-like representation as str.

    :param node: the AST node representing a compare expression
    :type node: ast.Compare
    :return: the readable code-like node build up
    :rtype: str
    """

    return ast.unparse(node)


def handle_assert(struct: StandardReturn, node: ast.Assert) -> StandardReturn:
    """
    Processes an `ast.Assert` node and returns its data.

    This function analyzes the components of an assertion, including the expression of
    the test and the optional message, returning a structured dict with the extracted
    details.

    Key elements of the returned data:
    - statement: The type of statement, identified as `Statement.Assert`;
    - test: A repr of the test expression being asserted;
    - msg: A string repr of the optional message, `None` if no message is provided.

    :param node: the AST node representing an assertion statement
    :type node: ast.Assert
    :return: a dict containing the statement type, test expression, and optional message
    :rtype: StandardReturn
    """

    statement: Final[Statement] = Statement.Assert
    test: str = cast(str, handle_node(node.test))
    msg: Final[str | None] = cast(str, handle_node(node.msg)) if node.msg else None
    code: Final[str] = ast.unparse(node)

    data: StandardReturn = standard_struct()

    data.update(
        {
            'statement': statement,
            'test': test,
            'msg': msg,
            'code': code,
        }
    )

    struct.update(data)

    return struct


def handle_list(node: ast.List) -> str:
    """
    Recieves an `ast.List` node and returns its code-like representation as str.

    :param node: the AST node representing a list expression
    :type node: ast.List
    :return: the readable code-like node build up
    :rtype: str
    """

    return ast.unparse(node)


def handle_tuple(node: ast.Tuple) -> str:
    """
    Recieves an `ast.Tuple` node and returns its code-like representation as str.

    :param node: the AST node representing a tuple expression
    :type node: ast.Tuple
    :return: the readable code-like node build up
    :rtype: str
    """

    return ast.unparse(node)


def handle_set(node: ast.Set) -> str:
    """
    Recieves an `ast.Set` node and returns its code-like representation as str.

    :param node: the AST node representing a set expression
    :type node: ast.Set
    :return: the readable code-like node build up
    :rtype: str
    """

    return ast.unparse(node)


def handle_dict(node: ast.Dict) -> str:
    """
    Recieves an `ast.Dict` node and returns its code-like representation as str.

    :param node: the AST node representing a dict expression
    :type node: ast.Dict
    :return: the readable code-like node build up
    :rtype: str
    """

    return ast.unparse(node)


def handle_subscript(node: ast.Subscript) -> str:
    """
    Recieves an `ast.Subscript` node and returns its code-like representation as str.

    :param node: the AST node representing a subscript expression
    :type node: ast.Subscript
    :return: the readable code-like node build up
    :rtype: str
    """

    return ast.unparse(node)


def handle_slice(node: ast.Slice) -> str:
    """
    Recieves an `ast.Slice` node and returns its code-like representation as str.

    :param node: the AST node representing a slice expression
    :type node: ast.Slice
    :return: the readable code-like node build up
    :rtype: str
    """

    return ast.unparse(node)


def handle_name(node: ast.Name) -> str:
    """
    Processes an `ast.Name` node and returns its data.

    This function just returns the node id, as str...

    :param node: the AST node representing an assignment statement
    :type node: ast.Name
    :return: the node id
    :rtype: str
    """

    return node.id
