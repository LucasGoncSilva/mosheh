import ast
from typing import Final, cast

from . import constants
from .custom_types import (
    ImportType,
    StandardReturn,
    StandardReturnProccessor,
    Statement,
)
from .utils import bin, is_lib_installed, standard_struct


def handle_def_nodes(node: ast.AST) -> list[StandardReturn]:
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

    :param node: The AST node to process.
    :type node: ast.AST
    :return: An object containing information associated with the node.
    :rtype: list[StandardReturn]
    """

    data: list[StandardReturn] = []

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
            lst.extend(cast(list[str], handle_node(i)))

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


def handle_node(
    node: ast.AST | ast.expr | None,
) -> list[StandardReturnProccessor] | None:
    """
    Processes various types of AST nodes and returns a standardized representation.

    This function extends the capabilities of `handle_def_nodes()` by supporting a
    wider range of Python Abstract Syntax Tree (AST) node types. It identifies the
    node type, delegates processing to the appropriate handler function, and
    accumulates the results into a standardized format.

    Key concepts:
    - AST Parsing: Supports multiple node types (e.g., imports, functions, classes,
      constants).
    - Dynamic Dispatch: Uses type-checking to delegate node handling to specific
      functions (e.g., `handle_import`, `handle_function_def`).
    - Data Standardization: Accumulates processed data into a consistent structure
      (`StandardReturnProccessor`).

    Example:
    ```python
    import ast

    source_code = 'def my_function():\\n    pass'
    node = ast.parse(source_code).body[0]
    result = handle_node(node)
    result
    # Outputs a standardized representation of the function definition.
    ```

    :param node: The AST node to be processed.
    :type node: ast.AST | ast.expr | None
    :return: A list of standardized data representing the processed node, or `None` if
                no node is provided.
    :rtype: list[StandardReturnProccessor] | None
    """

    if node is None:
        return node

    data: list[StandardReturnProccessor] = []

    def update_data(new_data: list[StandardReturn]):
        nonlocal data
        data = cast(list[StandardReturnProccessor], new_data)

    # -------------------------
    # Imports - ast.Import | ast.ImportFrom
    # -------------------------

    if isinstance(node, ast.Import):
        update_data(handle_import(cast(list[StandardReturn], data), node))
    elif isinstance(node, ast.ImportFrom):
        update_data(handle_import_from(cast(list[StandardReturn], data), node))

    # -------------------------
    # Constants - ast.Assign | ast.AnnAssign
    # -------------------------

    elif isinstance(node, ast.Assign):
        lst: list[str] = [
            cast(list[str], handle_constant([], i))[0]
            for i in node.targets
            if isinstance(i, ast.Constant)
        ]
        if any(map(str.isupper, lst)):
            update_data(handle_assign(cast(list[StandardReturn], data), node))
    elif isinstance(node, ast.AnnAssign):
        if isinstance(node.target, ast.Name) and node.target.id.isupper():
            update_data(handle_annassign(cast(list[StandardReturn], data), node))

    # -------------------------
    # Functions - ast.FunctionDef | ast.AsyncFunctionDef
    # -------------------------

    elif isinstance(node, ast.FunctionDef):
        update_data(handle_function_def(cast(list[StandardReturn], data), node))
    elif isinstance(node, ast.AsyncFunctionDef):
        update_data(handle_async_function_def(cast(list[StandardReturn], data), node))

    # -------------------------
    # Classes - ast.ClassDef
    # -------------------------

    elif isinstance(node, ast.ClassDef):
        update_data(handle_class_def(cast(list[StandardReturn], data), node))

    # -------------------------
    # Assertions - ast.Assert
    # -------------------------

    elif isinstance(node, ast.Assert):
        update_data(handle_assert(cast(list[StandardReturn], data), node))

    # -------------------------
    # Calls - ast.Call
    # -------------------------

    elif isinstance(node, ast.Call):
        data = handle_call(data, node)

    # -------------------------
    # Literals - ast.Constants
    # -------------------------

    elif isinstance(node, ast.Constant):
        data = handle_constant(data, node)

    # -------------------------
    # Attributes - ast.Attribute
    # -------------------------

    elif isinstance(node, ast.Attribute):
        data = handle_attribute(data, node)

    # -------------------------
    # Lists - ast.List
    # -------------------------

    elif isinstance(node, ast.List):
        data = handle_list(data, node)

    # -------------------------
    # Tuples - ast.Tuple
    # -------------------------

    elif isinstance(node, ast.Tuple):
        data = handle_tuple(data, node)

    # -------------------------
    # Sets - ast.Set
    # -------------------------

    elif isinstance(node, ast.Set):
        data = handle_set(data, node)

    # -------------------------
    # Dicts - ast.Dict
    # -------------------------

    elif isinstance(node, ast.Dict):
        data = handle_dict(data, node)

    # -------------------------
    # Basic Operations - "+", "-", "*", "/", ...
    # -------------------------

    elif isinstance(node, ast.BinOp):
        data = handle_binop(data, node)

    # -------------------------
    # Unary Operation
    # -------------------------

    elif isinstance(node, ast.UnaryOp):
        data = handle_unary(data, node)

    # -------------------------
    # SubScripts - ast.Subscript
    # -------------------------

    elif isinstance(node, ast.Subscript):
        data = handle_subscript(data, node)

    # -------------------------
    # Slices - ast.Slice
    # -------------------------

    elif isinstance(node, ast.Slice):
        data = handle_slice(data, node)

    # -------------------------
    # Names - ast.Name
    # -------------------------

    elif isinstance(node, ast.Name):
        data = handle_name(data, node)

    # -------------------------
    # Names - ast.Compare
    # -------------------------

    elif isinstance(node, ast.Compare):
        data = handle_compare(data, node)

    # -------------------------
    # Joined Strings - ast.JoinedStr
    # -------------------------

    elif isinstance(node, ast.JoinedStr):
        data = handle_joined_str(data, node)

    # -------------------------
    # Ternary Operator - ast.IfExp
    # -------------------------

    elif isinstance(node, ast.IfExp):
        data = handle_if_expression(data, node)

    # -------------------------
    # Boolean Operation (or) - ast.BoolOp
    # -------------------------

    elif isinstance(node, ast.BoolOp):
        data = handle_bool_op(data, node)

    # -------------------------
    # Comprehensions - ast.ListComp | ast.DictComp | ast.SetComp | ast.GeneratorExp
    # -------------------------

    elif isinstance(node, ast.ListComp | ast.DictComp | ast.SetComp | ast.GeneratorExp):
        data = handle_comprehensions(data, node)

    # -------------------------
    # Lambda Functions - ast.Lambda
    # -------------------------

    elif isinstance(node, ast.Lambda):
        data = handle_lambda(data, node)

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

    :param lib_name: The name of the library to be imported.
    :type lib_name: str
    :return: A standardized dictionary representing the import statement.
    :rtype: list[StandardReturn]
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


def handle_import(
    struct: list[StandardReturn], node: ast.Import
) -> list[StandardReturn]:
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

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturn]
    :param node: The AST node representing an import statement.
    :type node: ast.Import
    :return: The updated structure with information about the imported libraries.
    :rtype: list[StandardReturn]
    """

    for lib in [i.name for i in node.names]:
        struct.append(__handle_import(lib))

    return struct


def handle_import_from(
    struct: list[StandardReturn], node: ast.ImportFrom
) -> list[StandardReturn]:
    """
    Processes an `ast.ImportFrom` node and returnes its data.

    This function iterates over the imported module names within an `ast.ImportFrom`
    node, classifying each module into one of the following categorys, as
    `handle_import`:
    - Native: The module is a built-in Python module.
    - Third-Party: The module is installed via external libraries.
    - Local: The module is neither built-in nor a third-party library, problably local.

    Each module's data includes its path and category, stored in a structured dict.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturn]
    :param node: The AST node representing an import statement.
    :type node: ast.ImportFrom
    :return: A dict containing the statement type and categorized module information.
    :rtype: list[StandardReturn]
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

    for i in names:
        data: StandardReturn = standard_struct()
        data.update(
            {
                'statement': statement,
                'name': i,
                'path': path,
                'category': category,
                'code': code,
            }
        )

        struct.append(data)

    return struct


def handle_attribute(
    struct: list[StandardReturnProccessor], node: ast.Attribute
) -> list[StandardReturnProccessor]:
    """
    Recieves an `ast.Attribute` node and returns its code-like representation as str.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing a slice expression.
    :type node: ast.Attribute
    :return: The readable code-like node build up.
    :rtype: list[StandardReturnProccessor]
    """

    struct.append(ast.unparse(node))

    return struct


def handle_call(
    struct: list[StandardReturnProccessor], node: ast.Call
) -> list[StandardReturnProccessor]:
    """
    Recieves an `ast.Call` node and returns its code-like representation as str.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing a slice expression.
    :type node: ast.Call
    :return: The readable code-like node build up.
    :rtype: list[StandardReturnProccessor]
    """

    struct.append(ast.unparse(node))

    return struct


def handle_constant(
    struct: list[StandardReturnProccessor], node: ast.Constant
) -> list[StandardReturnProccessor]:
    """
    Recieves an `ast.Constant` node and returns its code-like representation as str.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing a slice expression.
    :type node: ast.Constant
    :return: The readable code-like node build up.
    :rtype: str
    """

    struct.append(ast.unparse(node))

    return struct


def handle_assign(
    struct: list[StandardReturn], node: ast.Assign
) -> list[StandardReturn]:
    """
    Processes an `ast.Assign` node and returns its data.

    This function analyzes the components of an assignment, including the target vars
    and the assigned value, returning a structured dict with the extracted details.

    Key elements of the returned data:
    - tokens: A list of string repr for all target variables in the assignment.
    - value: A string repr of the value being assigned.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturn]
    :param node: The AST node representing an assignment statement.
    :type node: ast.Assign
    :return: A dict containing the statement type, target variables, and assigned value.
    :rtype: list[StandardReturn]
    """

    statement: Final[Statement] = Statement.Assign
    tokens: Final[list[str]] = [
        cast(list[str], handle_node(i))[0] for i in node.targets
    ]
    value: Final[str] = cast(list[str], handle_node(node.value))[0]
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

    struct.append(data)

    return struct


def handle_binop(
    struct: list[StandardReturnProccessor], node: ast.BinOp
) -> list[StandardReturnProccessor]:
    """
    Recieves an `ast.BinOp` node and returns its code-like representation as str.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing a binary operation expression.
    :type node: ast.BinOp
    :return: The readable code-like node build up.
    :rtype: str
    """

    struct.append(ast.unparse(node))

    return struct


def handle_annassign(
    struct: list[StandardReturn], node: ast.AnnAssign
) -> list[StandardReturn]:
    """
    Processes an `ast.AnnAssign` node and returns its data.

    This function analyzes the components of an assignment, including the target var
    and the assigned value, plus the typing notation, returning a structured dict with
    the extracted details.

    Key elements of the returned data:
    - token: A string repr for the target var in the assignment.
    - value: A string repr of the value being assigned.
    - annot: The type hint for the assignment.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturn]
    :param node: The AST node representing an assignment statement.
    :type node: ast.AnnAssign
    :return: A dict with the statement type, target var, type hint and assigned value.
    :rtype: list[StandardReturn]
    """

    statement: Statement = Statement.AnnAssign
    name: str = cast(list[str], handle_node(node.target))[0]
    annot: str = cast(list[str], handle_node(node.annotation))[0]
    value: str = ''
    code: str = ast.unparse(node)

    if node.value is not None:
        value = cast(list[str], handle_node(node.value))[0]

    data: StandardReturn = standard_struct()

    data.update(
        {
            'statement': statement,
            'name': name,
            'annot': annot,
            'value': value,
            'code': code,
        }
    )

    struct.append(data)

    return struct


def __format_arg(name: str, annotation: str | None, default: str | None) -> str:
    """
    Formats a function argument into a string repr with optional type annotations and
    default values.

    This function constructs a f-string representing a function argument, including its
    name, optional type annotation, and default value. It ensures consistent formatting
    for use in function signatures or documentation.

    Key concepts:
    - Type Annotations: Adds type annotations if provided.
    - Default Values: Appends default values where applicable.
    - Fallback Handling: If neither an annotation nor a default value is present, it
      defaults to 'Unknown'.

    Example:
    ```python
    formatted = __format_arg('param', 'int', '42')
    formatted
    # "param: int = 42"
    ```

    :param name: The name of the argument.
    :type name: str
    :param annotation: The type annotation for the argument, if any.
    :type annotation: str | None
    :param default: The default value of the argument, if any.
    :type default: str | None
    :return: A formatted string representing the argument.
    :rtype: str
    """

    if annotation and default:
        return f'{name}: {annotation} = {default}'
    elif annotation:
        return f'{name}: {annotation}'
    elif default:
        return f'{name} = {default}'
    else:
        return f'{name}: Unknown'


def __process_function_args(node_args: ast.arguments) -> str:
    """
    Processes and formats positional arguments from a function definition.

    This function extracts positional arguments from an `ast.arguments` node,
    including their names, optional type annotations, and default values.
    It formats them into a single, comma-separated string repr suitable
    for documentation or code generation.

    Key concepts:
    - Positional Arguments: Handles arguments that can be passed by position.
    - Type Annotations: Extracts and formats type annotations, if present.
    - Default Values: Aligns each argument with its default value, if provided.

    Example:
    ```python
    import ast

    source = "def example(a: int, b: str = 'default'): pass"
    node = ast.parse(source).body[0]
    formatted = __process_function_args(node.args)
    formatted
    # "a: int, b: str = 'default'"
    ```

    :param node_args: The `arguments` node from an AST function definition.
    :type node_args: ast.arguments
    :return: A comma-separated string of formatted positional arguments.
    :rtype: str
    """

    formatted_args: list[str] = []

    for i, arg in enumerate(node_args.args):
        name: str = arg.arg
        annotation: str | None = (
            cast(list[str], handle_node(arg.annotation))[0] if arg.annotation else None
        )

        default = None
        if i < len(node_args.kw_defaults):
            default_node = node_args.kw_defaults[i]
            if default_node:
                default = str(cast(list[str], handle_node(default_node))[0])

        formatted_args.append(__format_arg(name, annotation, default))

    return ', '.join(formatted_args)


def __process_function_kwargs(node_args: ast.arguments) -> str:
    """
    Processes and formats keyword-only arguments from a function definition.

    This function extracts keyword-only arguments from an `ast.arguments` node,
    including their names, optional type annotations, and default values. It formats
    them into a single, comma-separated string repr suitable for documentation
    or code generation.

    Key concepts:
    - Keyword-only Arguments: Processes arguments that must be passed by keyword.
    - Type Annotations: Extracts and formats type annotations if present.
    - Default Values: Handles default values, aligning them with their own arguments.

    Example:
    ```python
    import ast

    source = 'def example(*, debug: bool = True): pass'
    node = ast.parse(source).body[0]
    formatted = __process_function_kwargs(node.args)
    formatted
    # "debug: bool = True"
    ```

    :param node_args: The `arguments` node from an AST function definition.
    :type node_args: ast.arguments
    :return: A comma-separated string of formatted keyword-only arguments.
    :rtype: str
    """

    formatted_kwargs: list[str] = []

    for i, arg in enumerate(node_args.kwonlyargs):
        name: str = arg.arg
        annotation: str | None = (
            cast(list[str], handle_node(arg.annotation))[0] if arg.annotation else None
        )

        default = None
        if i < len(node_args.kw_defaults):
            default_node = node_args.kw_defaults[i]
            if default_node:
                default = str(cast(list[str], handle_node(default_node))[0])

        formatted_kwargs.append(__format_arg(name, annotation, default))

    return ', '.join(formatted_kwargs)


def handle_function_def(
    struct: list[StandardReturn], node: ast.FunctionDef
) -> list[StandardReturn]:
    """
    Processes an `ast.FunctionDef` node and returns its data.

    This function analyzes the components of a func def, mapping the name, decorators,
    arguments (name, type, default value), return type and even the type of function it
    is:
    - Function: a base function, simply defined using `def` keyword;
    - Method: also base function, but defined inside a class (e.g. `def __init__():`);
    - Generator: process an iterable object at a time, on demand, with `yield` inside.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturn]
    :param node: The AST node representing a func def statement.
    :type node: ast.FunctionDef
    :return: A dict containing the statement type and the data listed before.
    :rtype: list[StandardReturn]
    """

    statement: Final[Statement] = Statement.FunctionDef
    name: Final[str] = node.name
    decos: Final[list[str]] = [
        cast(list[str], handle_node(i))[0] for i in node.decorator_list
    ]
    rtype: Final[str] | None = (
        cast(list[str], handle_node(node.returns))[0]
        if node.returns is not None
        else None
    )
    code: Final[str] = ast.unparse(node)

    args_str: str = __process_function_args(node.args)
    kwargs_str: str = __process_function_kwargs(node.args)

    data: StandardReturn = standard_struct()

    data.update(
        {
            'statement': statement,
            'name': name,
            'decorators': decos,
            'rtype': rtype,
            'args': args_str,
            'kwargs': kwargs_str,
            'code': code,
        }
    )

    struct.append(data)

    return struct


def handle_async_function_def(
    struct: list[StandardReturn],
    node: ast.AsyncFunctionDef,
) -> list[StandardReturn]:
    """
    Processes an `ast.AsyncFunctionDef` node and returns its data.

    This function analyzes the components of a func def, mapping the name, decorators,
    arguments (name, type, default value), return type and even the type of function it
    is, which in this case can be only one:
    - Coroutine: An async func, defined with `async def` syntax..

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturn]
    :param node: The AST node representing a func def statement.
    :type node: ast.AsyncFunctionDef
    :return: A dict containing the statement type and the data listed before.
    :rtype: list[StandardReturn]
    """

    statement: Final[Statement] = Statement.AsyncFunctionDef
    name: Final[str] = node.name
    decos: Final[list[str]] = [
        cast(list[str], handle_node(i))[0] for i in node.decorator_list
    ]
    rtype: Final[str] | None = (
        cast(list[str], handle_node(node.returns))[0]
        if node.returns is not None
        else None
    )
    code: Final[str] = ast.unparse(node)

    args_str: str = __process_function_args(node.args)
    kwargs_str: str = __process_function_kwargs(node.args)

    data: StandardReturn = standard_struct()

    data.update(
        {
            'statement': statement,
            'name': name,
            'decorators': decos,
            'rtype': rtype,
            'args': args_str,
            'kwargs': kwargs_str,
            'code': code,
        }
    )

    struct.append(data)

    return struct


def __format_class_kwarg(name: str | None, value: ast.expr) -> str:
    """
    Formats a kwarg from a class definition into a string repr.

    This function converts an AST kwarg into a string, representing it in the format
    `name=value`. If the keyword has no name (e.g., for positional arguments), only the
    value is returned.

    Key concepts:
    - AST Unparsing: Uses `ast.unparse` to convert an AST expression into its
      corresponding Python code as a string.
    - Conditional Formatting: Handles named and unnamed (positional) keyword arguments.

    Example:
    ```python
    import ast

    kwarg = ast.keyword(arg='debug', value=ast.Constant(value=True))
    formatted = __format_class_kwarg(kwarg.arg, kwarg.value)
    formatted
    # "debug = True"
    ```

    :param name: The name of the kwarg (can be `None` for positional arguments).
    :type name: str | None
    :param value: The AST expression representing the value of the keyword argument.
    :type value: ast.expr
    :return: A formatted string representing the keyword argument.
    :rtype: str
    """

    value_str: str = ast.unparse(value)
    if name:
        return f'{name} = {value_str}'
    return value_str


def __process_class_kwargs(keywords: list[ast.keyword]) -> str:
    """
    Processes and formats keyword arguments from a class definition.

    This function takes a list of keyword arguments (from an AST node) and formats
    them into a single, comma-separated string. Each keyword is processed using
    the `__format_class_kwarg` function to ensure consistent repr.

    Key concepts:
    - Keyword Formatting: Converts each kwarg into a string repr
      of the form `key=value`.
    - List Processing: Aggregates and joins all formatted keyword arguments into a
      single string for use in documentation or code generation.

    Example:
    ```python
    keywords = [ast.keyword(arg='name', value=ast.Constant(value='MyClass'))]
    formatted = __process_class_kwargs(keywords)
    formatted
    # "name='MyClass'"
    ```

    :param keywords: A list of AST keyword arguments.
    :type keywords: list[ast.keyword]
    :return: A comma-separated string of formatted keyword arguments.
    :rtype: str
    """

    formatted_kwargs: list[str] = [
        __format_class_kwarg(kw.arg, kw.value) for kw in keywords
    ]
    return ', '.join(formatted_kwargs)


def handle_class_def(
    struct: list[StandardReturn], node: ast.ClassDef
) -> list[StandardReturn]:
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

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturn]
    :param node: The AST node representing a class definition.
    :type node: ast.ClassDef
    :return: A dict with the statement type, name, base classes, decorators, and kwargs.
    :rtype: list[StandardReturn]
    """

    statement: Final[Statement] = Statement.ClassDef
    name: Final[str] = node.name
    inheritance: Final[list[str]] = [
        cast(list[str], handle_node(i))[0]
        for i in node.bases
        if isinstance(i, ast.Name)
    ]
    decos: Final[list[str]] = [
        cast(list[str], handle_node(i))[0] for i in node.decorator_list
    ]
    kwargs_str: str = __process_class_kwargs(node.keywords)
    code: Final[str] = ast.unparse(node)

    data: StandardReturn = standard_struct()

    data.update(
        {
            'statement': statement,
            'name': name,
            'inheritance': inheritance,
            'decorators': decos,
            'kwargs': kwargs_str,
            'code': code,
        }
    )

    struct.append(data)

    return struct


def handle_compare(
    struct: list[StandardReturnProccessor], node: ast.Compare
) -> list[StandardReturnProccessor]:
    """
    Recieves an `ast.Compare` node and returns its code-like representation as str.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing a compare expression.
    :type node: ast.Compare
    :return: The readable code-like node build up.
    :rtype: str
    """

    struct.append(ast.unparse(node))

    return struct


def handle_unary(
    struct: list[StandardReturnProccessor], node: ast.UnaryOp
) -> list[StandardReturnProccessor]:
    """
    Recieves an `ast.UnaryOp` node and returns its code-like representation as str.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing a compare expression.
    :type node: ast.UnaryOp
    :return: The readable code-like node build up.
    :rtype: str
    """

    struct.append(ast.unparse(node))

    return struct


def handle_assert(
    struct: list[StandardReturn], node: ast.Assert
) -> list[StandardReturn]:
    """
    Processes an `ast.Assert` node and returns its data.

    This function analyzes the components of an assertion, including the expression of
    the test and the optional message, returning a structured dict with the extracted
    details.

    Key elements of the returned data:
    - statement: The type of statement, identified as `Statement.Assert`;
    - test: A repr of the test expression being asserted;
    - msg: A string repr of the optional message, `None` if no message is provided.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturn]
    :param node: The AST node representing an assertion statement.
    :type node: ast.Assert
    :return: A dict with the statement type, test expression, and optional message.
    :rtype: list[StandardReturn]
    """

    statement: Final[Statement] = Statement.Assert
    test: str = cast(list[str], handle_node(node.test))[0]
    msg: Final[str | None] = (
        cast(list[str], handle_node(node.msg))[0] if node.msg else None
    )
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

    struct.append(data)

    return struct


def handle_list(
    struct: list[StandardReturnProccessor], node: ast.List
) -> list[StandardReturnProccessor]:
    """
    Recieves an `ast.List` node and returns its code-like representation as str.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing a list expression.
    :type node: ast.List
    :return: The readable code-like node build up.
    :rtype: str
    """

    struct.append(ast.unparse(node))

    return struct


def handle_tuple(
    struct: list[StandardReturnProccessor], node: ast.Tuple
) -> list[StandardReturnProccessor]:
    """
    Recieves an `ast.Tuple` node and returns its code-like representation as str.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing a tuple expression.
    :type node: ast.Tuple
    :return: The readable code-like node build up.
    :rtype: str
    """

    struct.append(ast.unparse(node))

    return struct


def handle_set(
    struct: list[StandardReturnProccessor], node: ast.Set
) -> list[StandardReturnProccessor]:
    """
    Recieves an `ast.Set` node and returns its code-like representation as str.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing a set expression.
    :type node: ast.Set
    :return: The readable code-like node build up.
    :rtype: str
    """

    struct.append(ast.unparse(node))

    return struct


def handle_dict(
    struct: list[StandardReturnProccessor], node: ast.Dict
) -> list[StandardReturnProccessor]:
    """
    Recieves an `ast.Dict` node and returns its code-like representation as str.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing a dict expression.
    :type node: ast.Dict
    :return: The readable code-like node build up.
    :rtype: str
    """

    struct.append(ast.unparse(node))

    return struct


def handle_subscript(
    struct: list[StandardReturnProccessor], node: ast.Subscript
) -> list[StandardReturnProccessor]:
    """
    Recieves an `ast.Subscript` node and returns its code-like representation as str.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing a subscript expression.
    :type node: ast.Subscript
    :return: The readable code-like node build up.
    :rtype: str
    """

    struct.append(ast.unparse(node))

    return struct


def handle_slice(
    struct: list[StandardReturnProccessor], node: ast.Slice
) -> list[StandardReturnProccessor]:
    """
    Recieves an `ast.Slice` node and returns its code-like representation as str.

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing a slice expression.
    :type node: ast.Slice
    :return: The readable code-like node build up.
    :rtype: list[StandardReturnProccessor]
    """

    struct.append(ast.unparse(node))

    return struct


def handle_name(
    struct: list[StandardReturnProccessor], node: ast.Name
) -> list[StandardReturnProccessor]:
    """
    Processes an `ast.Name` node and returns its data.

    This function just returns the node id, as str...

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing an assignment statement.
    :type node: ast.Name
    :return: The node id.
    :rtype: list[StandardReturnProccessor]
    """

    struct.append(ast.unparse(node))

    return struct


def handle_joined_str(
    struct: list[StandardReturnProccessor], node: ast.JoinedStr
) -> list[StandardReturnProccessor]:
    """
    Processes an `ast.JoinedStr` node and returns its data.

    This function just returns the node id, as str...

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing an assignment statement.
    :type node: ast.JoinedStr
    :return: The node id.
    :rtype: list[StandardReturnProccessor]
    """

    struct.append(ast.unparse(node))

    return struct


def handle_if_expression(
    struct: list[StandardReturnProccessor], node: ast.IfExp
) -> list[StandardReturnProccessor]:
    """
    Processes an `ast.IfExp` node and returns its data.

    This function just returns the node id, as str...

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing an assignment statement.
    :type node: ast.IfExp
    :return: The node id.
    :rtype: list[StandardReturnProccessor]
    """

    struct.append(ast.unparse(node))

    return struct


def handle_bool_op(
    struct: list[StandardReturnProccessor], node: ast.BoolOp
) -> list[StandardReturnProccessor]:
    """
    Processes an `ast.BoolOp` node and returns its data.

    This function just returns the node id, as str...

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing an assignment statement.
    :type node: ast.BoolOp
    :return: The node id.
    :rtype: list[StandardReturnProccessor]
    """

    struct.append(ast.unparse(node))

    return struct


def handle_comprehensions(
    struct: list[StandardReturnProccessor],
    node: ast.ListComp | ast.DictComp | ast.SetComp | ast.GeneratorExp,
) -> list[StandardReturnProccessor]:
    """
    Processes a comprehension node and returns its data.

    This function just returns the node id, as str...

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing an assignment statement.
    :type node: ast.BoolOp
    :return: The node id.
    :rtype: list[StandardReturnProccessor]
    """

    struct.append(ast.unparse(node))

    return struct


def handle_lambda(
    struct: list[StandardReturnProccessor], node: ast.Lambda
) -> list[StandardReturnProccessor]:
    """
    Processes an `ast.Lambda` node and returns its data.

    This function just returns the node id, as str...

    :param struct: The structure to be updated with statement details.
    :type struct: list[StandardReturnProccessor]
    :param node: The AST node representing an assignment statement.
    :type node: ast.Lambda
    :return: The node id.
    :rtype: list[StandardReturnProccessor]
    """

    struct.append(ast.unparse(node))

    return struct
