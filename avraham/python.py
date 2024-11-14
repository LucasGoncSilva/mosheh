from ast import Call, Name, parse
from ast import walk as astwalk
from os import path, walk
from types import ModuleType
from typing import Generator


def count_calls(dir_name: str, callable: str) -> int:
    count: int = 0

    for file in iterate_py(dir_name):
        with open(file, encoding='utf-8') as f:
            code: str = f.read()

        tree: ModuleType = parse(code, filename=file)

        for node in astwalk(tree):
            if isinstance(node, Call):
                if isinstance(node.func, Name) and node.func.id == callable:
                    count += 1

    return count


def iterate(root: str) -> Generator[str, str, str]:
    for dirpath, _, files in walk(root):
        for file in files:
            yield path.join(dirpath, file)


def iterate_py(root: str) -> Generator[str, str, str]:
    for file in iterate(root):
        if file.endswith('.py'):
            yield file


def handle_py(root: str) -> None: ...
