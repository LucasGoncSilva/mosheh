"""
This module provides functionality to analyze a Python codebase, extracting and
organizing its structural information.

The primary purpose of this module is to traverse a directory tree, identify Python
source files, and parse their abstract syntax trees (AST) to collect metadata about
their classes, functions, and methods. The gathered data is organized in a nested
dictionary format (`CodebaseDict`) to facilitate further processing and analysis.

Key Functions:

- `read_codebase`: Orchestrates the entire process by iterating through the codebase,
    parsing Python files, and storing structured information about their contents.

- `_mark_methods`: Annotates methods in class definitions with a `parent` attribute to
    link them back to their parent class.

- `encapsulated_mark_methods_for_unittest`: Exposes `_mark_methods` for external testing
    purposes.

- `_iterate`: Recursively yields file paths within the provided root directory for
    iteration.

How It Works:

1. The `read_codebase` function starts by invoking `_iterate` to traverse the directory
    tree starting from the given root path.

2. For each Python file encountered, the file is read, and its AST is parsed to extract
    relevant information.

3. The `_mark_methods` function adds parent annotations to methods inside class
    definitions to establish context.

4. The extracted data is processed using the `handle_def_nodes` function and added to
    the nested dictionary structure using utilities like `add_to_dict`.

5. The result is a comprehensive dictionary (`CodebaseDict`) containing all collected
    data, which is returned as a standard dictionary for compatibility.

This module is a foundational component for automated documentation generation,
providing the structural insights needed for subsequent steps in the documentation
pipeline.
"""

import ast
from collections.abc import Generator
from logging import Logger, getLogger
from os import path, sep, walk
from typing import Any

from mosheh.custom_types import CodebaseDict, FileRole, StandardReturn
from mosheh.handler import handle_def_nodes
from mosheh.utils import add_to_dict, convert_to_regular_dict, nested_dict


logger: Logger = getLogger('mosheh')


def read_codebase(root: str) -> CodebaseDict:
    """
    Iterates through the codebase and collects all info needed.

    Using `iterate()` to navigate and `handle_def_nodes()` to get data,
    stores the collected data in a dict of type CodebaseDict, defined
    in constants.py file.

    Also works as a dispatch-like, matching the files extensions,
    leading each file to its flow.

    :param root: The root path/dir to be iterated.
    :type root: str
    :return: All the codebase data collected.
    :rtype: CodebaseDict
    """

    codebase: CodebaseDict = nested_dict()

    logger.info(f'Starting iteration through {root}')
    for file in _iterate(root):
        logger.debug(f'Iterating: {file}')

        if file.endswith('.py'):
            logger.debug(f'.py: {file}')
            with open(file, encoding='utf-8') as f:
                code: str = f.read()
                logger.debug(f'{file} read')

            tree: ast.AST = ast.parse(code, filename=file)
            logger.debug('Code tree parsed')

            statements: list[StandardReturn] = []

            __meta__: StandardReturn = {
                '__role__': FileRole.PythonSourceCode,
                '__docstring__': 'No file docstring provided.',
            }

            for node in ast.walk(tree):
                logger.debug(f'Node: {type(node)}')
                if isinstance(node, ast.Module) and (
                    __docstring__ := ast.get_docstring(node)
                ):
                    __meta__['__docstring__'] = __docstring__
                elif isinstance(node, ast.ClassDef):
                    _mark_methods(node)
                elif isinstance(node, ast.FunctionDef) and getattr(
                    node, 'parent', None
                ):
                    continue

                data: list[StandardReturn] = handle_def_nodes(node)
                logger.debug('Node processed')

                if data:
                    statements.extend(data)
                    logger.debug('Node inserted into statement list')

            statements.insert(0, __meta__)

            add_to_dict(codebase, file.split(sep), statements)
            logger.debug(f'{file} stmts added to CodebaseDict')

    return convert_to_regular_dict(codebase)


def _mark_methods(node: ast.ClassDef) -> None:
    """
    Marks all `FunctionDef` nodes within a given `ClassDef` node by setting a
    `parent` attribute to indicate their association with the class.

    This function iterates over the child nodes of the provided class node, and
    for each method (a `FunctionDef`), it assigns the class type (`ast.ClassDef`)
    to the `parent` attribute of the method node.

    :param node: The class definition node containing methods to be marked.
    :type node: ast.ClassDef
    :return: No data to be returned
    :rtype: None
    """

    for child_node in ast.iter_child_nodes(node):
        if isinstance(child_node, ast.FunctionDef):
            setattr(child_node, 'parent', ast.ClassDef)


def encapsulated_mark_methods_for_unittest(node: ast.ClassDef) -> None:
    """
    Just encapsulates `_mark_methods` function to external use, only for unittesting.

    :param node: The class definition node containing methods to be marked.
    :type node: ast.ClassDef
    :return: No data to be returned
    :rtype: None
    """
    _mark_methods(node)


def _iterate(root: str) -> Generator[str, Any, Any]:
    """
    Iterates through every dir and file starting at provided root.

    Iterates using for-loop in os.walk and for dirpath and file in
    files yields the path for each file from the provided root to it.

    :param root: The root to be used as basedir.
    :type root: str
    :return: The path for each file on for-loop.
    :rtype: Generator[str, Any, Any]
    """

    for dirpath, _, files in walk(root):
        for file in files:
            yield path.join(dirpath, file)
