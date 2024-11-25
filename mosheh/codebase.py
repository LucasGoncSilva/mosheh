import ast
from os import path, sep, walk
from typing import Any, Generator

from custom_types import CodebaseDict, StandardReturn
from handlers import handle_def_nodes
from utils import add_to_dict, convert_to_regular_dict, nested_dict


def read_codebase(root: str) -> CodebaseDict:
    """
    Iterates through the codebase and collects all info needed.

    Using `iterate()` to navigate and `handle_def_nodes()` to get data,
    stores the collected data in a dict of type CodebaseDict, defined
    in constants.py file.

    Also works as a dispatch-like, matching the files extensions,
    leading each file to its flow.

    :param root: the root path/dir to be iterated
    :type root: str
    :return: all the codebase data collected
    :rtype: CodebaseDict
    """

    codebase: CodebaseDict = nested_dict()

    for file in iterate(root):
        if file.endswith('.py'):
            with open(file, encoding='utf-8') as f:
                code: str = f.read()

            tree: ast.AST = ast.parse(code, filename=file)

            statements: list[StandardReturn] = []

            for node in ast.walk(tree):
                data: StandardReturn = handle_def_nodes(node)

                if data != {}:
                    statements.append(data)

            add_to_dict(codebase, file.split(sep), statements)

    return convert_to_regular_dict(codebase)


def iterate(root: str) -> Generator[str, Any, Any]:
    """
    Iterates through every dir and file starting at provided root.

    Iterates using for-loop in os.walk and for dirpath and file in
    files yields the path for each file from the provided root to it.

    :param root: the root to be used as basedir
    :type root: str
    :return: the path for each file on for-loop
    :rtype: Generator[str, Any, Any]
    """

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
    calls: dict[str, list[str]] = {'funcs': [], 'classes': []}

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
