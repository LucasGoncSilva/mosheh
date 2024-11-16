import ast
from os import path, walk
from typing import Generator

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
    NodeHandlerDict,
    Statement,
)


def read_codebase(root) -> dict | None:
    codebase: dict[str, list[NodeHandlerDict]] = {}

    for file in iterate(root):
        if file.endswith('.py'):
            with open(file, encoding='utf-8') as f:
                code: str = f.read()

            tree: ast.AST = ast.parse(code, filename=file)

            statements: list[NodeHandlerDict] = []

            for node in ast.walk(tree):
                data: NodeHandlerDict = {}

                # -------------------------
                # Imports - Import | ImportFrom
                # -------------------------

                if isinstance(node, ast.Import):
                    data = handle_import(node)
                elif isinstance(node, ast.ImportFrom):
                    data = handle_import_from(node)

                # -------------------------
                # Constants - Assign | AnnAssign
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
                # Functions - FunctionDef/AsyncFunctionDef
                # -------------------------

                elif isinstance(node, ast.FunctionDef):
                    data = handle_function_def(node)
                elif isinstance(node, ast.AsyncFunctionDef):
                    data = handle_async_function_def(node)

                # -------------------------
                # Functions - FunctionDef/AsyncFunctionDef
                # -------------------------

                elif isinstance(node, ast.ClassDef):
                    data = handle_class_def(node)

                # -------------------------
                # Functions - FunctionDef/AsyncFunctionDef
                # -------------------------

                elif isinstance(node, ast.Assert):
                    data = handle_assert(node)

                statements.append(data)

            codebase[file] = statements

    print(codebase)


def iterate(root: str) -> Generator:
    for dirpath, _, files in walk(root):
        for file in files:
            yield path.join(dirpath, file)


def count_calls(dir_name: str, callable: str) -> int:
    count: int = 0

    for file in iterate(dir_name):
        with open(file, encoding='utf-8') as f:
            code: str = f.read()

        tree: ast.AST = ast.parse(code, filename=file)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == callable:
                    count += 1

    return count


def list_calls(dir_name: str) -> dict[str, list[str]]:
    calls = {'funcs': [], 'classes': []}

    for file in iterate(dir_name):
        with open(file, encoding='utf-8') as f:
            code = f.read()

        tree = ast.parse(code, filename=file)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name not in calls['funcs']:
                    calls['funcs'].append(func_name)
                # method_name = node.func
                # if method_name not in calls['funcs']:
                #     calls['funcs'].append(method_name)

            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Name):
                    class_name = node.value.func.id
                    if class_name not in calls['classes']:
                        calls['classes'].append(class_name)

    return calls


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


def handle_call(node: ast.Call) -> CallHandlerDict:
    call_obj: str = node.func.id

    args: list[str] = [i.id for i in node.args if isinstance(i, ast.Name)]
    args += [f'*{i.value.id}' for i in node.args if isinstance(i, ast.Starred)]

    kwargs: list[str] = []
    for param in node.keywords:
        if param.arg:
            kwargs.append(f'{param.value.id}={param.arg}')
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
    tokens: list[str] = [i.id for i in node.targets]
    value: str | CallHandlerDict = ''

    if isinstance(node.value, ast.Constant):
        value = handle_constant(node.value)
    elif isinstance(node.value, ast.Call):
        value = handle_call(node.value)

    data: AssignHandlerDict = {
        'statement': Statement.Assign,
        'tokens': tokens,
        'value': value,
    }

    return data


def handle_binop(node: ast.BinOp) -> BinOpHandlerDict:
    pre_left = node.left

    if isinstance(pre_left, ast.Constant):
        left = handle_constant(pre_left)
    elif isinstance(pre_left, ast.Call):
        left = handle_call(pre_left)

    pre_right = node.right

    if isinstance(pre_right, ast.Constant):
        right = handle_constant(pre_right)
    elif isinstance(pre_right, ast.Call):
        right = handle_call(pre_right)

    op: str = ''

    match type(node.op):
        case ast.Add:
            op += '+'
        case ast.Sub:
            op += '-'
        case ast.Mult:
            op += '*'
        case ast.Div:
            op += '/'
        case ast.FloorDiv:
            op += '//'
        case ast.Mod:
            op += '%'
        case ast.Pow:
            op += '**'
        case ast.LShift:
            op += '<<'
        case ast.RShift:
            op += '>>'
        case ast.BitOr:
            op += '|'
        case ast.BitXor:
            op += '^'
        case ast.BitAnd:
            op += '&'

    data: BinOpHandlerDict = {
        'statement': Statement.BinOp,
        'left': left,
        'op': op,
        'right': right,
    }

    return data


def handle_annassign(node: ast.AnnAssign) -> AnnAssignHandlerDict:
    token: str = node.target.id
    annot: str = node.annotation.id
    value = ''

    if isinstance(node.value, ast.Constant):
        value = handle_constant(node.value)
    elif isinstance(node.value, ast.Call):
        value = handle_call(node.value)

    data: AnnAssignHandlerDict = {
        'statement': Statement.AnnAssign,
        'token': token,
        'annot': annot,
        'value': value,
    }

    return data


def handle_function_def(node: ast.FunctionDef) -> FunctionDefHandlerDict:
    name: str = node.name
    decos: list[str] = [i.id for i in node.decorator_list]
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
            annot = node.args.vararg.annotation.id

        s_args = (name, annot, None)

    default_diff = len(node.args.args) - len(node.args.defaults)

    for i, arg in enumerate(node.args.args, start=1):
        name: str = arg.arg
        annot: str | None = arg.annotation.id if arg.annotation is not None else None
        default: str | CallHandlerDict | None = None

        if default_diff and i > default_diff:
            expected = node.args.defaults[i - 1 - default_diff]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)
        else:
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
            annot = node.args.kwarg.annotation.id

        ss_kwargs = (name, annot, None)

    kwdefault_diff = len(node.args.kwonlyargs) - len(node.args.kw_defaults)

    for i, arg in enumerate(node.args.kwonlyargs, start=1):
        name: str = arg.arg
        annot: str | None = arg.annotation.id if arg.annotation is not None else None
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
        if isinstance(node.returns, ast.Constant):
            rtype = handle_constant(node.returns)
        elif isinstance(node.returns, ast.Name):
            rtype = node.returns.id

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
    decos: list[str] = [i.id for i in node.decorator_list]
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
            annot = node.args.vararg.annotation.id

        s_args = (name, annot, None)

    default_diff = len(node.args.args) - len(node.args.defaults)

    for i, arg in enumerate(node.args.args, start=1):
        name: str = arg.arg
        annot: str | None = arg.annotation.id if arg.annotation is not None else None
        default: str | CallHandlerDict | None = None

        if default_diff and i > default_diff:
            expected = node.args.defaults[i - 1 - default_diff]

            if isinstance(expected, ast.Constant):
                default = handle_constant(expected)
            elif isinstance(expected, ast.Call):
                default = handle_call(expected)
        else:
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
            annot = node.args.kwarg.annotation.id

        ss_kwargs = (name, annot, None)

    kwdefault_diff = len(node.args.kwonlyargs) - len(node.args.kw_defaults)

    for i, arg in enumerate(node.args.kwonlyargs, start=1):
        name: str = arg.arg
        annot: str | None = arg.annotation.id if arg.annotation is not None else None
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
        if isinstance(node.returns, ast.Constant):
            rtype = handle_constant(node.returns)
        elif isinstance(node.returns, ast.Name):
            rtype = node.returns.id

    data: AsyncFunctionDefHandlerDict = {
        'statement': Statement.AsyncFunctionDef,
        'name': name,
        'decos': decos,
        'rtype': rtype,
        'arg_lst': arg_lst,
        'kwarg_lst': kwarg_lst,
    }

    return data


def handle_class_def(node: ast.ClassDef) -> ClassDefHandlerDict:
    name: str = node.name
    parents: list[str] = [i.id for i in node.bases]
    decos: list[str] = [i.id for i in node.decorator_list]

    kwargs: list[tuple] = [(i.arg, i.value.id) for i in node.keywords]

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
    if isinstance(node.test, ast.Name):
        test = node.test.id
    elif isinstance(node.test, ast.Compare):
        test = handle_compare(node.test)
    elif isinstance(node.test, ast.Call):
        test = handle_call(node.test)

    msg: str | None = node.msg.id if node.msg else None

    data: AssertHandlerDict = {
        'statement': Statement.Assert,
        'test': test,
        'msg': msg,
    }

    return data
