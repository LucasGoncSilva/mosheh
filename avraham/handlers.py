from typing import cast
import ast

import constants
from custom_types import (
    AnnAssignHandlerDict,
    AssertHandlerDict,
    AssignHandlerDict,
    AsyncFunctionDefHandlerDict,
    BinOpHandlerDict,
    CallHandlerDict,
    ClassDefHandlerDict,
    CompareHandlerDict,
    FunctionDefHandlerDict,
    ImportFromHandlerDict,
    ImportHandlerDict,
    ImportType,
    ListHandlerDict,
    NodeHandler,
    SetHandlerDict,
    SubscriptHandlerDict,
    SliceHandlerDict,
    Statement,
    TupleHandlerDict,
    DictHandlerDict,
)


def handle_def_nodes(node: ast.AST) -> NodeHandler:
    data: NodeHandler = {}

    # -------------------------
    # Imports - ast.Import | ast.ImportFrom
    # -------------------------

    if isinstance(node, ast.Import):
        data = handle_import(node)
    elif isinstance(node, ast.ImportFrom):
        data = handle_import_from(node)

    # -------------------------
    # Constants - ast.Assign | ast.AnnAssign
    # -------------------------

    elif isinstance(node, ast.Assign) and any(
        map(str.isupper, [i.id for i in node.targets if isinstance(i, ast.Constant)])
    ):
        data = handle_assign(node)
    elif (
        isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id.isupper()
    ):
        data = handle_annassign(node)

    # -------------------------
    # Functions - ast.FunctionDef | ast.AsyncFunctionDef
    # -------------------------

    elif isinstance(node, ast.FunctionDef):
        data = handle_function_def(node)
    elif isinstance(node, ast.AsyncFunctionDef):
        data = handle_async_function_def(node)

    # -------------------------
    # Classes - ast.ClassDef
    # -------------------------

    elif isinstance(node, ast.ClassDef):
        data = handle_class_def(node)

    # -------------------------
    # Assertions - ast.Assert
    # -------------------------

    elif isinstance(node, ast.Assert):
        data = handle_assert(node)

    return data


def handle_node(node: ast.AST) -> NodeHandler:
    data: NodeHandler = {}

    # -------------------------
    # Imports - ast.Import | ast.ImportFrom
    # -------------------------

    if isinstance(node, ast.Import):
        data = handle_import(node)
    elif isinstance(node, ast.ImportFrom):
        data = handle_import_from(node)

    # -------------------------
    # Constants - ast.Assign | ast.AnnAssign
    # -------------------------

    elif isinstance(node, ast.Assign) and any(
        map(str.isupper, [i.id for i in node.targets])
    ):
        data = handle_assign(node)
    elif (
        isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id.isupper()
    ):
        data = handle_annassign(node)

    # -------------------------
    # Functions - ast.FunctionDef | ast.AsyncFunctionDef
    # -------------------------

    elif isinstance(node, ast.FunctionDef):
        data = handle_function_def(node)
    elif isinstance(node, ast.AsyncFunctionDef):
        data = handle_async_function_def(node)

    # -------------------------
    # Classes - ast.ClassDef
    # -------------------------

    elif isinstance(node, ast.ClassDef):
        data = handle_class_def(node)

    # -------------------------
    # Assertions - ast.Assert
    # -------------------------

    elif isinstance(node, ast.Assert):
        data = handle_assert(node)

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

    return data


def handle_import(node: ast.Import) -> ImportHandlerDict:
    mods = {'modules': {}}

    for mod in [i.name for i in node.names]:
        mod_data = {}

        if mod in constants.BUILTIN_MODULES:
            mod_data['categorie'] = ImportType.Native
            mod_data['path'] = None

        mods['modules'][mod] = mod_data.copy()

    data: ImportHandlerDict = {'statement': Statement.Import, **mods}

    return data


def handle_import_from(node: ast.ImportFrom) -> ImportFromHandlerDict:
    mods = {
        'path': node.module,
        'modules': [i.name for i in node.names],
    }

    if f'{node.module}.'.split('.')[0] in constants.BUILTIN_MODULES:
        mods['categorie'] = ImportType.Native
        mods['path'] = None

    data: ImportFromHandlerDict = {'statement': Statement.ImportFrom, **mods}

    return data


def handle_attribute(node: ast.Attribute) -> str:
    return f'{node.value}.{node.attr}'


def handle_call(node: ast.Call) -> CallHandlerDict:
    call_obj = handle_node(node.func)

    args: list[str] = [handle_node(i) for i in node.args]
    args += [
        f'*{handle_node(i.value)}' for i in node.args if isinstance(i, ast.Starred)
    ]

    kwargs: list[str] = []
    for param in node.keywords:
        if param.arg:
            kwargs.append(f'{handle_node(param.value)}={param.arg}')
        else:
            kwargs.append(f'**{param.arg}')

    data: CallHandlerDict = {
        'statement': Statement.Call,
        'call_obj': call_obj,
        'args': args,
        'kwargs': kwargs,
    }

    return data


def handle_constant(node: ast.Constant) -> str:
    return node.value


def handle_assign(node: ast.Assign) -> AssignHandlerDict:
    tokens: list[NodeHandler] = [handle_node(i) for i in node.targets]

    value: NodeHandler = handle_node(node.value)

    data: AssignHandlerDict = {
        'statement': Statement.Assign,
        'tokens': tokens,
        'value': value,
    }

    return data


def handle_binop(node: ast.BinOp) -> BinOpHandlerDict:
    left = handle_node(node.left)
    right = handle_node(node.right)

    dispatch: dict = {
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

    op: str = cast(str, dispatch.get(type(node.op)))

    data: BinOpHandlerDict = {
        'statement': Statement.BinOp,
        'left': left,
        'op': op,
        'right': right,
    }

    return data


def handle_annassign(node: ast.AnnAssign) -> AnnAssignHandlerDict:
    token: NodeHandler = handle_node(node.target)
    annot: NodeHandler = handle_node(node.annotation)
    value = ''

    if isinstance(node.value, ast.Constant):
        value = handle_constant(node.value)
    elif isinstance(node.value, ast.Call):
        value = handle_call(node.value)

    return {
        'statement': Statement.AnnAssign,
        'token': token,
        'annot': annot,
        'value': value,
    }


def handle_function_def(node: ast.FunctionDef) -> FunctionDefHandlerDict:
    name: str = node.name
    decos: list[str] = [handle_node(i) for i in node.decorator_list]
    rtype: str | None = None
    arg_lst: list[tuple[str, str | None, str | CallHandlerDict | None]] = []
    s_args: tuple[str | None, str | None, None] | None = None
    kwarg_lst = []
    ss_kwargs = None

    has_star_args: bool = True if node.args.vararg is not None else False
    has_star_star_kwargs: bool = True if node.args.kwarg is not None else False

    if has_star_args:
        name: str = f'*{node.args.vararg.arg}'
        annot: str | None = None

        if node.args.vararg.annotation is not None:
            annot = handle_node(node.args.vararg.annotation)

        s_args = (name, annot, None)

    default_diff = len(node.args.args) - len(node.args.defaults)

    for i, arg in enumerate(node.args.args, start=1):
        name: str = arg.arg
        annot: str | None = None
        default: str | CallHandlerDict | None = None

        if arg.annotation is not None:
            handle_node(arg.annotation)

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

        arg_lst.append((name, annot, default))

    if has_star_args:
        arg_lst.insert(len(arg_lst), s_args)

    if has_star_star_kwargs:
        name: str = f'*{node.args.kwarg.arg}'
        annot: str | None = None

        if node.args.kwarg.annotation is not None:
            annot = handle_node(node.args.kwarg.annotation)

        ss_kwargs = (name, annot, None)

    kwdefault_diff = len(node.args.kwonlyargs) - len(node.args.kw_defaults)

    for i, arg in enumerate(node.args.kwonlyargs, start=1):
        name: str = arg.arg
        annot: NodeHandler | None = (
            handle_node(arg.annotation) if arg.annotation is not None else None
        )
        default: str | CallHandlerDict | None = None

        if kwdefault_diff and i > kwdefault_diff:
            expected = node.args.kw_defaults[i - 1 - kwdefault_diff]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)
        else:
            expected = node.args.kw_defaults[i - 1]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)

        kwarg_lst.append((name, annot, default))

    if has_star_args:
        kwarg_lst.insert(len(kwarg_lst), ss_kwargs)

    if node.returns is not None:
        rtype = handle_node(node.returns)

    data: FunctionDefHandlerDict = {
        'statement': Statement.FunctionDef,
        'name': name,
        'decos': decos,
        'rtype': rtype,
        'arg_lst': arg_lst,
        'kwarg_lst': kwarg_lst,
    }

    return data


def handle_async_function_def(
    node: ast.AsyncFunctionDef,
) -> AsyncFunctionDefHandlerDict:
    name: str = node.name
    decos: list[str] = [handle_node(i) for i in node.decorator_list]
    rtype: str | None = None
    arg_lst: list[tuple[str, str | None, str | CallHandlerDict | None]] = []
    s_args: tuple[str | None, str | None, None] | None = None
    kwarg_lst = []
    ss_kwargs = None

    has_star_args: bool = True if node.args.vararg is not None else False
    has_star_star_kwargs: bool = True if node.args.kwarg is not None else False

    if has_star_args:
        name: str = f'*{node.args.vararg.arg}'
        annot: str | None = None

        if node.args.vararg.annotation is not None:
            annot = handle_node(node.args.vararg.annotation)

        s_args = (name, annot, None)

    default_diff = len(node.args.args) - len(node.args.defaults)

    for i, arg in enumerate(node.args.args, start=1):
        name: str = arg.arg
        annot: str | None = None
        default: str | CallHandlerDict | None = None

        if arg.annotation is not None:
            handle_node(arg.annotation)

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

        arg_lst.append((name, annot, default))

    if has_star_args:
        arg_lst.insert(len(arg_lst), s_args)

    if has_star_star_kwargs:
        name: str = f'*{node.args.kwarg.arg}'
        annot: str | None = None

        if node.args.kwarg.annotation is not None:
            annot = handle_node(node.args.kwarg.annotation)

        ss_kwargs = (name, annot, None)

    kwdefault_diff = len(node.args.kwonlyargs) - len(node.args.kw_defaults)

    for i, arg in enumerate(node.args.kwonlyargs, start=1):
        name: str = arg.arg
        annot: NodeHandler | None = (
            handle_node(arg.annotation) if arg.annotation is not None else None
        )
        default: str | CallHandlerDict | None = None

        if kwdefault_diff and i > kwdefault_diff:
            expected = node.args.kw_defaults[i - 1 - kwdefault_diff]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)
        else:
            expected = node.args.kw_defaults[i - 1]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)

        kwarg_lst.append((name, annot, default))

    if has_star_args:
        kwarg_lst.insert(len(kwarg_lst), ss_kwargs)

    if node.returns is not None:
        rtype = handle_node(node.returns)

    data: FunctionDefHandlerDict = {
        'statement': Statement.FunctionDef,
        'name': name,
        'decos': decos,
        'rtype': rtype,
        'arg_lst': arg_lst,
        'kwarg_lst': kwarg_lst,
    }

    return data


def handle_class_def(node: ast.ClassDef) -> ClassDefHandlerDict:
    name: str = node.name
    parents: list[str] = [handle_node(i) for i in node.bases if isinstance(i, ast.Name)]
    decos: list[str] = [handle_node(i) for i in node.decorator_list]

    kwargs: list[tuple] = [(i.arg, i.value) for i in node.keywords]

    data: ClassDefHandlerDict = {
        'statement': Statement.ClassDef,
        'name': name,
        'parents': parents,
        'decos': decos,
        'kwargs': kwargs,
    }

    return data


def handle_compare(node: ast.Compare) -> CompareHandlerDict:
    left: str | CallHandlerDict = ''
    if isinstance(node.left, ast.Constant):
        left = handle_constant(node.left)
    elif isinstance(node.left, ast.Call):
        left = handle_call(node.left)

    ops: list[str] = []

    for op in node.ops:
        match op:
            case ast.Eq:
                ops.append('=')
            case ast.NotEq:
                ops.append('!=')
            case ast.Lt:
                ops.append('<')
            case ast.LtE:
                ops.append('<=')
            case ast.Gt:
                ops.append('>')
            case ast.GtE:
                ops.append('>=')
            case ast.Is:
                ops.append('is')
            case ast.IsNot:
                ops.append('is not')
            case ast.In:
                ops.append('in')
            case ast.NotIn:
                ops.append('not in')

    operators: list[CallHandlerDict | str] = []

    for i in node.comparators:
        if isinstance(i, ast.Call):
            operators.append(handle_call(i))
        elif isinstance(i, ast.Constant):
            operators.append(handle_constant(i))

    data: CompareHandlerDict = {
        'statement': Statement.Compare,
        'left': left,
        'ops': ops,
        'operators': operators,
    }

    return data


def handle_assert(node: ast.Assert) -> AssertHandlerDict:
    test = handle_node(node.test)

    msg: str | None = handle_node(node.msg) if node.msg else None

    data: AssertHandlerDict = {
        'statement': Statement.Assert,
        'test': test,
        'msg': msg,
    }

    return data


def handle_list(node: ast.List) -> ListHandlerDict:
    return {
        'statement': Statement.List,
        'elements': [handle_node(i) for i in node.elts],
    }


def handle_tuple(node: ast.Tuple) -> TupleHandlerDict:
    return {
        'statement': Statement.Tuple,
        'elements': [handle_node(i) for i in node.elts],
    }


def handle_set(node: ast.Set) -> SetHandlerDict:
    return {
        'statement': Statement.Set,
        'elements': [handle_node(i) for i in node.elts],
    }


def handle_dict(node: ast.Dict) -> DictHandlerDict:
    keys = [handle_node(i) for i in node.keys]
    values = [handle_node(i) for i in node.values]

    if None in keys:
        values[-1] = f'**{values[-1]}'

    return {
        'statement': Statement.Dict,
        'keys': keys,
        'values': values,
    }


def handle_subscript(node: ast.Subscript) -> SubscriptHandlerDict:
    return {
        'statement': Statement.Subscript,
        'value': node.value,
        'slice': handle_node(node.slice),
    }


def handle_slice(node: ast.Slice) -> SliceHandlerDict:
    return {
        'statement': Statement.Slice,
        'lower': handle_node(node.lower),
        'upper': handle_node(node.upper),
    }


def handle_name(node: ast.Name) -> str:
    return node.id
