import ast
from typing import cast

import constants
from utils import bin, is_lib_installed
from custom_types import (
    AnnAssignHandlerDict,
    AssertHandlerDict,
    AssignHandlerDict,
    AsyncFunctionDefHandlerDict,
    BinOpHandlerDict,
    ArgList,
    CallHandlerDict,
    ClassDefHandlerDict,
    CompareHandlerDict,
    DictHandlerDict,
    AssertTest,
    FunctionDefHandlerDict,
    ImportFromHandlerDict,
    ImportHandlerDict,
    BinOperand,
    ImportType,
    ListHandlerDict,
    NodeHandler,
    SetHandlerDict,
    SliceHandlerDict,
    Statement,
    SubscriptHandlerDict,
    AnnAssignValue,
    TupleHandlerDict,
    ListItem,
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

    elif isinstance(node, ast.Assign):
        lst: list[str] = [
            handle_constant(i) for i in node.targets if isinstance(i, ast.Constant)
        ]
        if any(map(str.isupper, lst)):
            data = handle_assign(node)
    elif isinstance(node, ast.AnnAssign):
        if isinstance(node.target, ast.Name) and node.target.id.isupper():
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


def handle_node(node: ast.AST | ast.expr | None) -> NodeHandler | None:
    if node is None:
        return node

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

    elif isinstance(node, ast.Assign):
        lst: list[str] = [
            handle_constant(i) for i in node.targets if isinstance(i, ast.Constant)
        ]
        if any(map(str.isupper, lst)):
            data = handle_assign(node)
    elif isinstance(node, ast.AnnAssign):
        if isinstance(node.target, ast.Name) and node.target.id.isupper():
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
    mods: ImportHandlerDict = {'modules': {}}

    for mod in [i.name for i in node.names]:
        mod_data = {}
        mod_data['path'] = None

        if bin(mod, constants.BUILTIN_MODULES):
            mod_data['categorie'] = ImportType.Native
        elif is_lib_installed(mod):
            mod_data['categorie'] = ImportType.TrdParty
        else:
            mod_data['categorie'] = ImportType.Local

        mods['modules'][mod] = mod_data.copy()

    return {'statement': Statement.Import, **mods}


def handle_import_from(node: ast.ImportFrom) -> ImportFromHandlerDict:
    mods: ImportFromHandlerDict = {
        'modules': [i.name for i in node.names],
    }
    mods['path'] = node.module

    mod: str = f'{node.module}'
    print(mod)

    if mod.startswith('.'):
        mods['categorie'] = ImportType.Local
    elif bin(
        f'{mod}.'.split('.')[0],
        constants.BUILTIN_MODULES,
    ):
        mods['categorie'] = ImportType.Native
    elif is_lib_installed(mod):
        mods['categorie'] = ImportType.TrdParty
    else:
        mods['categorie'] = ImportType.Local

    return {'statement': Statement.ImportFrom, **mods}


def handle_attribute(node: ast.Attribute) -> str:
    return f'{node.value}.{node.attr}'


def handle_call(node: ast.Call) -> CallHandlerDict:
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
    return node.value


def handle_assign(node: ast.Assign) -> AssignHandlerDict:
    tokens: list[str] = [cast(str, handle_node(i)) for i in node.targets]

    value: str = cast(str, handle_node(node.value))

    return {
        'statement': Statement.Assign,
        'tokens': tokens,
        'value': value,
    }


def handle_binop(node: ast.BinOp) -> BinOpHandlerDict:
    left: BinOperand = cast(BinOperand, handle_node(node.left))
    right: BinOperand = cast(BinOperand, handle_node(node.right))

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

    return {
        'statement': Statement.BinOp,
        'left': left,
        'op': op,
        'right': right,
    }


def handle_annassign(node: ast.AnnAssign) -> AnnAssignHandlerDict:
    token: str = cast(str, handle_node(node.target))
    annot: str = cast(str, handle_node(node.annotation))
    value: AnnAssignValue = ''

    if node.value is not None:
        value = cast(AnnAssignValue, handle_node(node.value))

    return {
        'statement': Statement.AnnAssign,
        'token': token,
        'annot': annot,
        'value': value,
    }


def handle_function_def(node: ast.FunctionDef) -> FunctionDefHandlerDict:
    name: str = node.name
    decos: list[str] = [cast(str, handle_node(i)) for i in node.decorator_list]
    rtype: str | None = (
        cast(str, handle_node(node.returns)) if node.returns is not None else None
    )
    arg_lst: ArgList = []
    s_args: tuple[str | None, str | None, None] | None = None
    kwarg_lst: ArgList = []
    ss_kwargs: tuple[str | None, str | None, None] | None = None

    has_star_args: bool = True if node.args.vararg is not None else False
    has_star_star_kwargs: bool = True if node.args.kwarg is not None else False

    if has_star_args and node.args.vararg is not None:
        name: str = f'*{node.args.vararg.arg}'
        annot: str | None = None

        if node.args.vararg.annotation is not None:
            annot = cast(str, handle_node(node.args.vararg.annotation))

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

    if has_star_args and s_args is not None:
        arg_lst.insert(len(arg_lst), s_args)

    if has_star_star_kwargs and node.args.kwarg is not None:
        name: str = f'*{node.args.kwarg.arg}'
        annot: str | None = None

        if node.args.kwarg.annotation is not None:
            annot = cast(str, handle_node(node.args.kwarg.annotation))

        ss_kwargs = (name, annot, None)

    kwdefault_diff = len(node.args.kwonlyargs) - len(node.args.kw_defaults)

    for i, arg in enumerate(node.args.kwonlyargs, start=1):
        name: str = arg.arg
        annot: str | None = (
            cast(str, handle_node(arg.annotation))
            if arg.annotation is not None
            else None
        )
        default: str | CallHandlerDict | None = None

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

        kwarg_lst.append((name, annot, default))

    if has_star_star_kwargs and ss_kwargs is not None:
        kwarg_lst.insert(len(kwarg_lst), ss_kwargs)

    return {
        'statement': Statement.FunctionDef,
        'name': name,
        'decos': decos,
        'rtype': rtype,
        'arg_lst': arg_lst,
        'kwarg_lst': kwarg_lst,
    }


def handle_async_function_def(
    node: ast.AsyncFunctionDef,
) -> AsyncFunctionDefHandlerDict:
    name: str = node.name
    decos: list[str] = [cast(str, handle_node(i)) for i in node.decorator_list]
    rtype: str | None = (
        cast(str, handle_node(node.returns)) if node.returns is not None else None
    )
    arg_lst: ArgList = []
    s_args: tuple[str | None, str | None, None] | None = None
    kwarg_lst: ArgList = []
    ss_kwargs: tuple[str | None, str | None, None] | None = None

    has_star_args: bool = True if node.args.vararg is not None else False
    has_star_star_kwargs: bool = True if node.args.kwarg is not None else False

    if has_star_args and node.args.vararg is not None:
        name: str = f'*{node.args.vararg.arg}'
        annot: str | None = None

        if node.args.vararg.annotation is not None:
            annot = cast(str, handle_node(node.args.vararg.annotation))

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

    if has_star_args and s_args is not None:
        arg_lst.insert(len(arg_lst), s_args)

    if has_star_star_kwargs and node.args.kwarg is not None:
        name: str = f'*{node.args.kwarg.arg}'
        annot: str | None = None

        if node.args.kwarg.annotation is not None:
            annot = cast(str, handle_node(node.args.kwarg.annotation))

        ss_kwargs = (name, annot, None)

    kwdefault_diff = len(node.args.kwonlyargs) - len(node.args.kw_defaults)

    for i, arg in enumerate(node.args.kwonlyargs, start=1):
        name: str = arg.arg
        annot: str | None = (
            cast(str, handle_node(arg.annotation))
            if arg.annotation is not None
            else None
        )
        default: str | CallHandlerDict | None = None

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

        kwarg_lst.append((name, annot, default))

    if has_star_star_kwargs and ss_kwargs is not None:
        kwarg_lst.insert(len(kwarg_lst), ss_kwargs)

    return {
        'statement': Statement.AsyncFunctionDef,
        'name': name,
        'decos': decos,
        'rtype': rtype,
        'arg_lst': arg_lst,
        'kwarg_lst': kwarg_lst,
    }


def handle_class_def(node: ast.ClassDef) -> ClassDefHandlerDict:
    name: str = node.name
    parents: list[str] = [
        cast(str, handle_node(i)) for i in node.bases if isinstance(i, ast.Name)
    ]
    decos: list[str] = [cast(str, handle_node(i)) for i in node.decorator_list]
    kwargs: list[tuple[str, str]] = [
        cast(tuple[str, str], (i.arg, i.value)) for i in node.keywords
    ]

    return {
        'statement': Statement.ClassDef,
        'name': name,
        'parents': parents,
        'decos': decos,
        'kwargs': kwargs,
    }


def handle_compare(node: ast.Compare) -> CompareHandlerDict:
    left: str | CallHandlerDict = cast(str | CallHandlerDict, handle_node(node.left))

    dispatch: dict[type, str] = {
        ast.Eq: '=',
        ast.NotEq: '!=',
        ast.Lt: '<',
        ast.LtE: '<=',
        ast.Gt: '>',
        ast.GtE: '>=',
        ast.Is: 'is',
        ast.IsNot: 'is not',
        ast.In: 'in',
        ast.NotIn: 'not in',
    }
    ops: list[str] = []

    for op in node.ops:
        ops.append(dispatch[type(op)])

    operators: list[CallHandlerDict | str] = []

    for i in node.comparators:
        operators.append(cast(CallHandlerDict | str, handle_node(i)))

    return {
        'statement': Statement.Compare,
        'left': left,
        'ops': ops,
        'operators': operators,
    }


def handle_assert(node: ast.Assert) -> AssertHandlerDict:
    test: AssertTest = cast(AssertTest, handle_node(node.test))

    msg: str | None = cast(str, handle_node(node.msg)) if node.msg else None

    return {
        'statement': Statement.Assert,
        'test': test,
        'msg': msg,
    }


def handle_list(node: ast.List) -> ListHandlerDict:
    return {
        'statement': Statement.List,
        'elements': [cast(ListItem, handle_node(i)) for i in node.elts],
    }


def handle_tuple(node: ast.Tuple) -> TupleHandlerDict:
    return {
        'statement': Statement.Tuple,
        'elements': [cast(ListItem, handle_node(i)) for i in node.elts],
    }


def handle_set(node: ast.Set) -> SetHandlerDict:
    return {
        'statement': Statement.Set,
        'elements': [cast(ListItem, handle_node(i)) for i in node.elts],
    }


def handle_dict(node: ast.Dict) -> DictHandlerDict:
    keys: list[str] = [cast(str, handle_node(i)) for i in node.keys]
    values: list[str] = [cast(str, handle_node(i)) for i in node.values]

    if None in node.keys:
        values[-1] = f'**{values[-1]}'

    return {
        'statement': Statement.Dict,
        'keys': keys,
        'values': values,
    }


def handle_subscript(node: ast.Subscript) -> SubscriptHandlerDict:
    return {
        'statement': Statement.Subscript,
        'value': cast(str, handle_node(node.value)),
        'slice': cast(SliceHandlerDict, handle_node(node.slice)),
    }


def handle_slice(node: ast.Slice) -> SliceHandlerDict:
    return {
        'statement': Statement.Slice,
        'lower': cast(str, handle_node(node.lower)),
        'upper': cast(str, handle_node(node.upper)),
    }


def handle_name(node: ast.Name) -> str:
    return node.id
