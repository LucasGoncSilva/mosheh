import ast
from os import path, walk
from typing import Generator

import constants
from custom_types import ImportHandlerDict, ImportType, Statement


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
                    data: dict = handle_import(node)
                    print(data)
                elif isinstance(node, ast.ImportFrom):
                    path_to: str = str(node.module)
                    modules: list[str] = [i.name for i in node.names]
                    print(f"ImportFrom - module: '{path_to}', {modules}")

                # -------------------------
                # Constants - Assign | AnnAssign
                # -------------------------

                elif isinstance(node, ast.Assign):
                    print(f'Assign - {node} = {node.value}')
                elif (
                    isinstance(node, ast.AnnAssign)
                    and isinstance(node.target, ast.Name)
                    and node.target.id.isupper()
                ):
                    name: str = node.target.id
                    typ: str = node.annotation.id
                    value: str = ''
                    if isinstance(node.value, ast.Constant):
                        value += node.value.value
                    elif isinstance(node.value, ast.Call):
                        value += node.value.func.id
                        if isinstance(node.value.args[0], ast.BinOp):
                            left: str = node.value.args[0].left.func.id
                            right: str = node.value.args[0].right.func.id

                            op: str = ''

                            match type(node.value.args[0].op):
                                case ast.Add:
                                    op += '+'
                                case ast.Sub:
                                    op += '-'
                                case ast.Mult:
                                    op += '*'
                                case ast.Div:
                                    op += '/'

                            value += f'({left} {op} {right})'
                    print(f'AnnAssign - {name}: {typ} = {value}')

            # Get constants - Assign
            # Get functions - FunctionDef/AsyncFunctionDef
            # Get classes - ClassDef
            # Get assertions - Assert


def iterate(root: str) -> Generator[str, str]:
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
