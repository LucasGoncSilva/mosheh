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

- `_iterate`: Recursively yields file paths within the provided root directory for
    iteration.

How It Works:

1. The `read_codebase` function starts by invoking `_iterate` to navigate into the
    directory tree starting from the given root path.

2. For each file encountered, if a valid extension, the file is read and its AST or
    content - if not a programming language file - is parsed to extract relevant
    information.

3. The result is a comprehensive dictionary (`CodebaseDict`) containing all collected
    data, which is returned as a standard dictionary for compatibility.

This module is a foundational component for automated documentation generation,
providing the structural insights needed for subsequent steps in the documentation
pipeline.
"""

from collections import defaultdict
from collections.abc import Generator
from logging import Logger, getLogger
from os import path, walk
from typing import Any

from mosheh.handlers import handle_python_file
from mosheh.types.basic import CodebaseDict
from mosheh.utils import convert_to_regular_dict, nested_dict


logger: Logger = getLogger('mosheh')


def read_codebase(root: str) -> CodebaseDict:
    """
    Iterates through the codebase and collects all info possibly needed.

    Using `_iterate()` to navigate, stores the collected data in a dict
    of type CodebaseDict, matching the file type and processing based
    on it.

    Also works as a dispatch-like, matching the files extensions,
    leading each file to its flow.

    :param root: The root path/dir to be iterated.
    :type root: str
    :return: All the codebase data collected.
    :rtype: CodebaseDict
    """

    codebase: defaultdict[Any, Any] = nested_dict()

    logger.info(f'Starting iteration through {root}')
    for file in _iterate(root):
        logger.debug(f'Iterating: {file}')

        if file.endswith('.py'):
            logger.debug(f'.py: {file}')
            codebase = handle_python_file(codebase, file)

    return convert_to_regular_dict(codebase)


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
