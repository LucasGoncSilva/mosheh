# ruff: noqa: E501

from ast import AST, ClassDef, FunctionDef, parse, walk
from pathlib import Path
from typing import Any

from mosheh.codebase import encapsulated_mark_methods_for_unittest
from mosheh.handler import handle_std_nodes
from mosheh.types.basic import (
    StandardReturn,
)
from mosheh.types.enums import (
    FunctionType,
    ImportType,
    Statement,
)


def test_handle_std_nodes() -> None:
    with open(f'{Path(__file__).parent}/mock.py.txt', encoding='utf-8') as f:
        code: str = f.read()

    tree: AST = parse(code)
    statements: list[StandardReturn] = []

    for node in walk(tree):
        if isinstance(node, ClassDef):
            encapsulated_mark_methods_for_unittest(node)

        if isinstance(node, FunctionDef) and getattr(node, 'parent', None):
            continue

        data: list[StandardReturn] = handle_std_nodes(node)

        if data:
            statements.extend(data)

    expected: list[dict[str, Any]] = [
        {
            'statement': Statement.Import,
            'name': 'math',
            'path': None,
            'category': ImportType.Native,
            'code': 'import math',
        },
        {
            'statement': Statement.Import,
            'name': 'os.path',
            'path': None,
            'category': ImportType.TrdParty,
            'code': 'import os.path',
        },
        {
            'statement': Statement.ImportFrom,
            'name': 'defaultdict',
            'path': 'collections',
            'category': ImportType.Native,
            'code': 'from collections import defaultdict, namedtuple',
        },
        {
            'statement': Statement.ImportFrom,
            'name': 'namedtuple',
            'path': 'collections',
            'category': ImportType.Native,
            'code': 'from collections import defaultdict, namedtuple',
        },
        {
            'statement': Statement.ImportFrom,
            'name': 'List',
            'path': 'typing',
            'category': ImportType.Native,
            'code': 'from typing import List, Optional, Generator',
        },
        {
            'statement': Statement.ImportFrom,
            'name': 'Optional',
            'path': 'typing',
            'category': ImportType.Native,
            'code': 'from typing import List, Optional, Generator',
        },
        {
            'statement': Statement.ImportFrom,
            'name': 'Generator',
            'path': 'typing',
            'category': ImportType.Native,
            'code': 'from typing import List, Optional, Generator',
        },
        {
            'statement': Statement.Assign,
            'tokens': ['GLOBAL_CONSTANT'],
            'value': '42',
            'code': 'GLOBAL_CONSTANT = 42',
        },
        {
            'statement': Statement.Assign,
            'tokens': ['PI'],
            'value': 'math.pi',
            'code': 'PI = math.pi',
        },
        {
            'statement': Statement.ClassDef,
            'name': 'ExampleClass',
            'docstring': 'A simple example class.',
            'inheritance': [],
            'decorators': [],
            'kwargs': '',
            'code': 'class ExampleClass:\n    """A simple example class."""\n\n    class NestedClass:\n        """A nested class."""\n\n        def __init__(self, value: int):\n            self.value = value\n\n    def __init__(self, data: str, optional_data: Optional[int]=None):\n        self.data = data\n        self.optional_data = optional_data\n        self._private_attr = \'Private\'\n\n    def instance_method(self) -> str:\n        """An instance method."""\n        return f\'Data: {self.data}\'\n\n    @classmethod\n    def class_method(cls):\n        """A class method."""\n        return \'This is a class method.\'\n\n    @staticmethod\n    def static_method():\n        """A static method."""\n        return \'This is a static method.\'',
        },
        {
            'statement': Statement.FunctionDef,
            'docstring': 'A simple function.',
            'name': 'simple_function',
            'category': FunctionType.Function,
            'decorators': [],
            'rtype': 'int',
            'args': 'a: int, b: int',
            'kwargs': '',
            'code': 'def simple_function(a: int, b: int) -> int:\n    """A simple function."""\n    return a + b',
        },
        {
            'statement': Statement.FunctionDef,
            'docstring': 'A generator function.',
            'name': 'generator_function',
            'category': FunctionType.Generator,
            'decorators': [],
            'rtype': 'Generator[int, None, None]',
            'args': '',
            'kwargs': '',
            'code': 'def generator_function() -> Generator[int, None, None]:\n    """A generator function."""\n    for i in range(10):\n        yield i',
        },
        {
            'statement': Statement.AsyncFunctionDef,
            'docstring': 'An asynchronous function.',
            'name': 'async_function',
            'category': FunctionType.Coroutine,
            'decorators': [],
            'rtype': 'str',
            'args': 'url: str',
            'kwargs': '',
            'code': 'async def async_function(url: str) -> str:\n    """An asynchronous function."""\n    import aiohttp\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as response:\n            return await response.text()',
        },
        {
            'statement': Statement.FunctionDef,
            'docstring': 'A simple decorator.',
            'name': 'decorator_function',
            'category': FunctionType.Function,
            'decorators': [],
            'rtype': None,
            'args': 'func: Unknown',
            'kwargs': '',
            'code': 'def decorator_function(func):\n    """A simple decorator."""\n\n    def wrapper(*args, **kwargs):\n        print(\'Function is being called\')\n        return func(*args, **kwargs)\n    return wrapper',
        },
        {
            'statement': Statement.FunctionDef,
            'docstring': 'A decorated function.',
            'name': 'decorated_function',
            'category': FunctionType.Function,
            'decorators': ['decorator_function'],
            'rtype': None,
            'args': '',
            'kwargs': '',
            'code': '@decorator_function\ndef decorated_function():\n    """A decorated function."""\n    print(\'Hello, decorated world!\')',
        },
        {
            'statement': Statement.Assert,
            'test': 'x == 5',
            'msg': "'x should be 5'",
            'code': "assert x == 5, 'x should be 5'",
        },
        {
            'statement': Statement.FunctionDef,
            'docstring': None,
            'name': 'annotated_function',
            'category': FunctionType.Function,
            'decorators': [],
            'rtype': 'List[int]',
            'args': 'a: int, b: str',
            'kwargs': '',
            'code': 'def annotated_function(a: int, b: str) -> List[int]:\n    return [1, 2, 3]',
        },
        {
            'statement': Statement.FunctionDef,
            'docstring': 'A function with a docstring example.\n\nExample:\n    result = example_usage_function(1, 2)\n    print(result)  # Outputs 3',
            'name': 'example_usage_function',
            'category': FunctionType.Function,
            'decorators': [],
            'rtype': 'int',
            'args': 'a: int, b: int',
            'kwargs': '',
            'code': 'def example_usage_function(a: int, b: int) -> int:\n    """\n    A function with a docstring example.\n\n    Example:\n        result = example_usage_function(1, 2)\n        print(result)  # Outputs 3\n    """\n    return a + b',
        },
        {
            'statement': Statement.FunctionDef,
            'docstring': 'A function with an ellipsis.',
            'name': 'ellipsis_function',
            'category': FunctionType.Function,
            'decorators': [],
            'rtype': None,
            'args': 'a: Unknown, b: Unknown, c: Unknown',
            'kwargs': '',
            'code': 'def ellipsis_function(a, b, c=...):\n    """A function with an ellipsis."""\n    pass',
        },
        {
            'statement': Statement.ClassDef,
            'name': 'NestedClass',
            'docstring': 'A nested class.',
            'inheritance': [],
            'decorators': [],
            'kwargs': '',
            'code': 'class NestedClass:\n    """A nested class."""\n\n    def __init__(self, value: int):\n        self.value = value',
        },
        {
            'statement': Statement.FunctionDef,
            'docstring': None,
            'name': '__init__',
            'category': FunctionType.Method,
            'decorators': [],
            'rtype': None,
            'args': 'self: Unknown, data: str, optional_data: Optional[int]',
            'kwargs': '',
            'code': "def __init__(self, data: str, optional_data: Optional[int]=None):\n    self.data = data\n    self.optional_data = optional_data\n    self._private_attr = 'Private'",
        },
        {
            'statement': Statement.FunctionDef,
            'docstring': 'An instance method.',
            'name': 'instance_method',
            'category': FunctionType.Method,
            'decorators': [],
            'rtype': 'str',
            'args': 'self: Unknown',
            'kwargs': '',
            'code': 'def instance_method(self) -> str:\n    """An instance method."""\n    return f\'Data: {self.data}\'',
        },
        {
            'statement': Statement.FunctionDef,
            'docstring': 'A class method.',
            'name': 'class_method',
            'category': FunctionType.Method,
            'decorators': ['classmethod'],
            'rtype': None,
            'args': 'cls: Unknown',
            'kwargs': '',
            'code': '@classmethod\ndef class_method(cls):\n    """A class method."""\n    return \'This is a class method.\'',
        },
        {
            'statement': Statement.FunctionDef,
            'docstring': 'A static method.',
            'name': 'static_method',
            'category': FunctionType.Method,
            'decorators': ['staticmethod'],
            'rtype': None,
            'args': '',
            'kwargs': '',
            'code': '@staticmethod\ndef static_method():\n    """A static method."""\n    return \'This is a static method.\'',
        },
        {
            'statement': Statement.Import,
            'name': 'aiohttp',
            'path': None,
            'category': ImportType.Local,
            'code': 'import aiohttp',
        },
        {
            'statement': Statement.FunctionDef,
            'docstring': None,
            'name': 'wrapper',
            'category': FunctionType.Function,
            'decorators': [],
            'rtype': None,
            'args': '',
            'kwargs': '',
            'code': "def wrapper(*args, **kwargs):\n    print('Function is being called')\n    return func(*args, **kwargs)",
        },
        {
            'statement': Statement.FunctionDef,
            'docstring': None,
            'name': '__init__',
            'category': FunctionType.Method,
            'decorators': [],
            'rtype': None,
            'args': 'self: Unknown, value: int',
            'kwargs': '',
            'code': 'def __init__(self, value: int):\n    self.value = value',
        },
    ]

    assert len(statements) == len(expected)

    for i in statements:
        assert i in expected
