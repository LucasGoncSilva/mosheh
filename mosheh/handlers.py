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
    Processes an `ast.Import` node and returnes its data.

    This function iterates over the imported module names within an `ast.Import` node,
    classifying each module into one of the following categorys:
    - Native: The module is a built-in Python module.
    - Third-Party: The module is installed via external libraries.
    - Local: The module is neither built-in nor a third-party library, problably local.

    Each module's data includes its path (defaulting to `None`) and category, stored
    in a structured dict.

    :param node: the AST node representing an import statement
    :type node: ast.Import
    :return: a dict containing the statement type and categorized module information
    :rtype: ImportHandlerDict
    """

    for lib in [i.name for i in node.names]:
        struct.update(__handle_import(lib))

    return struct  # BUG: returns only last element -> change to list and return list struct


def handle_import_from(struct: StandardReturn, node: ast.ImportFrom) -> StandardReturn:
    """
    Processes an `ast.ImportFrom` node and returnes its data.

    This function iterates over the imported module names within an `ast.ImportFrom`
    node, classifying each module into one of the following categorys, as
    `handle_import`:
    - Native: The module is a built-in Python module.
    - Third-Party: The module is installed via external libraries.
    - Local: The module is neither built-in nor a third-party library, problably local.

    Each module's data includes its path (defaulting to `None`) and category, stored
    in a structured dict.

    :param node: the AST node representing an import statement
    :type node: ast.ImportFrom
    :return: a dict containing the statement type and categorized module information
    :rtype: ImportFromHandlerDict
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
    Processes an `ast.Constant` node and returns its data.

    This function just returns the node value, followed by its attr, as str in the form
    of f'{value}.{attr}'

    :param node: the AST node representing an assignment statement
    :type node: ast.Attribute
    :return: the node value folowed by its attr
    :rtype: str
    """

    return f'{node.value}.{node.attr}'


def handle_call(node: ast.Call) -> StandardReturn:
    """
    Processes an `ast.Call` node and returns its data.

    This function analyzes the components of a call expression, including the callable
    object, positional arguments, and keyword arguments, returning a structured
    dict with the extracted details.

    Key elements of the returned data:
    - call_obj: A string repr of the callable object.
    - args: A list of string repr for all positional args, also starred arguments.
    - kwargs: A list of string repr for all kwargs, formatted as `value=key` pairs.
    If the argument uses `**`, it is included with just the parameter name.

    :param node: the AST node representing a function or method call
    :type node: ast.Call
    :return: A dict with the statement type and details of the call expression
    :rtype: CallHandlerDict
    """

    call_obj: str = cast(str, handle_node(node.func))

    args: list[str] = [cast(str, handle_node(i)) for i in node.args]
    args += [
        f'*{handle_node(i.value)}' for i in node.args if isinstance(i, ast.Starred)
    ]

    kwargs: list[str] = []
    for param in node.keywords:
        if param.arg:
            kwargs.append(f'{handle_node(param.value)}={param.arg}')
        else:
            kwargs.append(f'**{param.arg}')

    return {
        'statement': Statement.Call,
        'call_obj': call_obj,
        'args': args,
        'kwargs': kwargs,
    }


def handle_constant(node: ast.Constant) -> str:
    """
    Processes an `ast.Constant` node and returns its data.

    This function just returns the node value, as str...

    :param node: the AST node representing an assignment statement
    :type node: ast.Constant
    :return: the node value
    :rtype: str
    """

    return node.value


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
    :rtype: AssignHandlerDict
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
    Processes an `ast.BinOp` node and returnes its data.

    This function maps the left and right operands and the operator itself, based on
    possible values for them, following the type notation for each:
    - `left` and `right` are operands annotated with `BinOperand`;
    - `op`, on the other hand, is an operator, one of below:
        - '+' - `ast.Add`
        - '-' - `ast.Sub`
        - '*' - `ast.Mult`
        - '/' - `ast.Div`
        - '//' - `ast.FloorDiv`
        - '%' - `ast.Mod`
        - '**' - `ast.Pow`
        - '<<' - `ast.LShift`
        - '>>' - `ast.RShift`
        - '|' - `ast.BitOr`
        - '^' - `ast.BitXor`
        - '&' - `ast.BitAnd`

    :param node: the AST node representing an import statement
    :type node: ast.BinOp
    :return: a dict containing the statement type and categorized module information
    :rtype: BinOpHandlerDict
    """

    left: StandardReturnProccessor = cast(
        StandardReturnProccessor, handle_node(node.left)
    )
    right: StandardReturnProccessor = cast(
        StandardReturnProccessor, handle_node(node.right)
    )

    dispatch: dict[type, str] = {
        ast.Add: '+',
        ast.Sub: '-',
        ast.Mult: '*',
        ast.Div: '/',
        ast.FloorDiv: '//',
        ast.Mod: '%',
        ast.Pow: '**',
        ast.LShift: '<<',
        ast.RShift: '>>',
        ast.BitOr: '|',
        ast.BitXor: '^',
        ast.BitAnd: '&',
    }

    op: str = dispatch[type(node.op)]

    return f'{left} {op} {right}'


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
    :rtype: AnnAssignHandlerDict
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
    :rtype: FunctionDefHandlerDict
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
        default: str | StandardReturn | None = None

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
        default: str | StandardReturn | None = None

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
            'decos': decos,
            'rtype': rtype,
            'arg': arg_lst,
            'kwarg': kwarg_lst,
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
    :rtype: AsyncFunctionDefHandlerDict
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
        default: str | StandardReturn | None = None

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
        default: str | StandardReturn | None = None

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
            'decos': decos,
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
    :rtype: ClassDefHandlerDict
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
            'decos': decos,
            'kwargs': kwargs,
            'code': code,
        }
    )

    struct.update(data)

    return struct


def handle_compare(node: ast.Compare) -> str:
    """
    Processes an `ast.Compare` node and returns its data.

    This function analyzes the components of a comparison operation, including the
    left-hand operand, comparison operators, and right-hand operands, returning a
    structured dict with the extracted details.

    Key elements of the returned data:
    - left: A string or `CallHandlerDict` repr of the left-hand operand;
    - ops: List of string reprs of the comparison operators -> `==`, `!=`, `<`, `>`;
    - operators: List of string or `CallHandlerDict` reprs of the right-hand operands.

    :param node: the AST node representing a comparison expression
    :type node: ast.Compare
    :return: A dict with the statement type, left-right-hand operands and operators
    :rtype: CompareHandlerDict
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
    :rtype: AssertHandlerDict
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


def handle_list(node: ast.List) -> StandardReturn:
    """
    Processes an `ast.List` node and returns its data.

    This function analyzes the elements of a list and returns a structured dict
    containing the details of the list and its components.

    Key elements of the returned data:
    - statement: The type of statement, identified as `Statement.List`;
    - elements: A list of reprs for each element in the list.

    :param node: the AST node representing a list expression
    :type node: ast.List
    :return: a dict containing the statement type and the list's elements
    :rtype: ListHandlerDict
    """

    return {
        'statement': Statement.List,
        'elements': [cast(str, handle_node(i)) for i in node.elts],
    }


def handle_tuple(node: ast.Tuple) -> StandardReturn:
    """
    Processes an `ast.Tuple` node and returns its data.

    This function analyzes the elements of a tuple and returns a structured dict
    containing the details of the tuple and its components.

    Key elements of the returned data:
    - statement: The type of statement, identified as `Statement.Tuple`;
    - elements: A list of reprs for each element in the tuple.

    :param node: the AST node representing a list expression
    :type node: ast.Tuple
    :return: a dict containing the statement type and the tuple's elements
    :rtype: TupleHandlerDict
    """

    return {
        'statement': Statement.Tuple,
        'elements': [cast(str, handle_node(i)) for i in node.elts],
    }


def handle_set(node: ast.Set) -> StandardReturn:
    """
    Processes an `ast.Set` node and returns its data.

    This function analyzes the elements of a set and returns a structured dict
    containing the details of the set and its components.

    Key elements of the returned data:
    - statement: The type of statement, identified as `Statement.Set`;
    - elements: A list of reprs for each element in the set.

    :param node: the AST node representing a list expression
    :type node: ast.Set
    :return: a dict containing the statement type and the set's elements
    :rtype: SetHandlerDict
    """
    return {
        'statement': Statement.Set,
        'elements': [cast(str, handle_node(i)) for i in node.elts],
    }


def handle_dict(node: ast.Dict) -> StandardReturn:
    """
    Processes an `ast.Dict` node and returns its data.

    This function analyzes the elements of a dict and returns a structured dict
    containing the details of the dict and its components.

    Key elements of the returned data:
    - statement: The type of statement, identified as `Statement.Dict`;
    - keys: A list of reprs for each key in the dict.
    - values: A list of reprs for each value in the dict.

    :param node: the AST node representing a list expression
    :type node: ast.Dict
    :return: a dict containing the statement type and the dict's elements
    :rtype: DictHandlerDict
    """

    keys: list[str] = [cast(str, handle_node(i)) for i in node.keys]
    values: list[str] = [cast(str, handle_node(i)) for i in node.values]

    if None in node.keys:
        values[-1] = f'**{values[-1]}'

    return {
        'statement': Statement.Dict,
        'keys': keys,
        'values': values,
    }


def handle_subscript(node: ast.Subscript) -> str:
    """
    Processes an `ast.Subscript` node and returns its data.

    This function analyzes the elements a subscript statement, returning a dict
    containing the details of the subscript and its components.

    Key elements of the returned data:
    - statement: The type of statement, identified as `Statement.Subscript`;
    - value: A str for the value of the subscript.
    - slice: A SliceHandlerDict object for the slice itself.

    :param node: the AST node representing a list expression
    :type node: ast.Subscript
    :return: a dict containing the statement type and the slice's elements
    :rtype: SubscriptHandlerDict
    """

    name: str = cast(str, handle_node(node.value))
    _slice: StandardReturnProccessor | None = handle_node(node.slice)

    return f'{name}[{_slice}]'


def handle_slice(node: ast.Slice) -> str:
    """
    Processes an `ast.Slice` node and returns its data.

    This function analyzes the elements a slice statement, returning a dict containing
    the details of the slice itself and its components.

    Key elements of the returned data:
    - statement: The type of statement, identified as `Statement.Slice`;
    - lower: A str for the lower value.
    - upper: A str for the upper value.

    :param node: the AST node representing a list expression
    :type node: ast.Slice
    :return: a dict containing the statement type and the slice's elements
    :rtype: SliceHandlerDict
    """

    lower: str = cast(str, handle_node(node.lower))
    upper: str = cast(str, handle_node(node.upper))
    step: str = ''

    if node.step is not None:
        value: str = cast(str, handle_node(node.step))
        step = f', {value}'

    return f'{lower}:{upper}{step}'


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
