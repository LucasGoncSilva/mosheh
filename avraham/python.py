import ast
from os import path, walk
from typing import Generator

from custom_types import NodeHandler
from handlers import handle_def_nodes


def read_codebase(root) -> dict | None:
    codebase: dict[str, list[NodeHandler]] = {}

    for file in iterate(root):
        if file.endswith('.py'):
            with open(file, encoding='utf-8') as f:
                code: str = f.read()

            tree: ast.AST = ast.parse(code, filename=file)

            statements: list[NodeHandler] = []

            for node in ast.walk(tree):
                data: NodeHandler = handle_def_nodes(node)

                if data != {}:
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
