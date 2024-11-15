import ast
from os import path, walk
from typing import Generator

import constants
from custom_types import (
    AnnAssignHandlerDict,
    AssignHandlerDict,
    BinOpHandlerDict,
    CallHandlerDict,
    FunctionDefHandlerDict,
    ImportFromHandlerDict,
    ImportHandlerDict,
    ImportType,
    NodeHandlerDict,
    Statement,
)


def read_codebase(root) -> dict | None:
    for file in iterate(root):
        if file.endswith('.py'):
            with open(file, encoding='utf-8') as f:
                code: str = f.read()

            tree: ast.AST = ast.parse(code, filename=file)

            for node in ast.walk(tree):
                # -------------------------
                # Imports - Import | ImportFrom
                # -------------------------

                if isinstance(node, ast.Import):
                    data: NodeHandlerDict = handle_import(node)
                    print(data)
                elif isinstance(node, ast.ImportFrom):
                    data: NodeHandlerDict = handle_import_from(node)
                    print(data)

                # -------------------------
                # Constants - Assign | AnnAssign
                # -------------------------

                elif isinstance(node, ast.Assign) and any(
                    map(str.isupper, [i.id for i in node.targets])
                ):
                    data = handle_assign(node)
                    print(data)
                elif (
                    isinstance(node, ast.AnnAssign)
                    and isinstance(node.target, ast.Name)
                    and node.target.id.isupper()
                ):
                    data = handle_annassign(node)
                    print(data)

                # -------------------------
                # Functions - FunctionDef/AsyncFunctionDef
                # -------------------------

                elif isinstance(node, ast.FunctionDef):
                    data = handle_function_def(node)
                    print(data)

            # Get functions - FunctionDef/AsyncFunctionDef
            # Get classes - ClassDef
            # Get assertions - Assert


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
    mods = {'path': node.module, 'modules': [i.name for i in node.names]}

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

    if node.returns is not None:
        if isinstance(node.returns, ast.Constant):
            rtype = handle_constant(node.returns)
        elif isinstance(node.returns, ast.Name):
            rtype = node.returns.id

    args: list[str] = []
    kwargs: list[str] = []

    data: FunctionDefHandlerDict = {
        'statement': Statement.FunctionDef,
        'name': name,
        'decos': decos,
        'rtype': rtype,
        'args': args,
        'kwargs': kwargs,
    }

    return data
