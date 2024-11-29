import ast
from collections.abc import Generator
from os import path, sep, walk
from typing import Any

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
                data: list[StandardReturn] = handle_def_nodes(node)

                if data:
                    statements.extend(data)

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
