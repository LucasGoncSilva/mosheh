# ruff: noqa: E501

from ast import AST, ClassDef, FunctionDef, parse, walk
from pathlib import Path
from typing import Any

from mosheh.handlers.python import (
    wrapped_handle_std_nodes_for_testing,
    wrapped_mark_methods_for_testing,
)
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
            wrapped_mark_methods_for_testing(node)

        if isinstance(node, FunctionDef) and getattr(node, 'parent', None):
            continue

        data: list[StandardReturn] = wrapped_handle_std_nodes_for_testing(node)

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
            'category': ImportType.Native,
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
            'name': '__init__',
            'category': FunctionType.Method,
            'docstring': None,
            'decorators': [],
            'rtype': None,
            'args': 'self: Unknown, data: str, optional_data: Optional[int]',
            'kwargs': '',
            'code': "def __init__(self, data: str, optional_data: Optional[int]=None):\n    self.data = data\n    self.optional_data = optional_data\n    self._private_attr = 'Private'",
        },
        {
            'statement': Statement.FunctionDef,
            'name': 'instance_method',
            'category': FunctionType.Method,
            'docstring': 'An instance method.',
            'decorators': [],
            'rtype': 'str',
            'args': 'self: Unknown',
            'kwargs': '',
            'code': 'def instance_method(self) -> str:\n    """An instance method."""\n    return f\'Data: {self.data}\'',
        },
        {
            'statement': Statement.FunctionDef,
            'name': 'class_method',
            'category': FunctionType.Method,
            'docstring': 'A class method.',
            'decorators': ['classmethod'],
            'rtype': None,
            'args': 'cls: Unknown',
            'kwargs': '',
            'code': '@classmethod\ndef class_method(cls):\n    """A class method."""\n    return \'This is a class method.\'',
        },
        {
            'statement': Statement.FunctionDef,
            'name': 'static_method',
            'category': FunctionType.Method,
            'docstring': 'A static method.',
            'decorators': ['staticmethod'],
            'rtype': None,
            'args': '',
            'kwargs': '',
            'code': '@staticmethod\ndef static_method():\n    """A static method."""\n    return \'This is a static method.\'',
        },
        {
            'statement': Statement.FunctionDef,
            'name': 'simple_function',
            'category': FunctionType.Function,
            'docstring': 'A simple function.',
            'decorators': [],
            'rtype': 'int',
            'args': 'a: int, b: int',
            'kwargs': '',
            'code': 'def simple_function(a: int, b: int) -> int:\n    """A simple function."""\n    return a + b',
        },
        {
            'statement': Statement.FunctionDef,
            'name': 'generator_function',
            'category': FunctionType.Generator,
            'docstring': 'A generator function.',
            'decorators': [],
            'rtype': 'Generator[int, None, None]',
            'args': '',
            'kwargs': '',
            'code': 'def generator_function() -> Generator[int, None, None]:\n    """A generator function."""\n    for i in range(10):\n        yield i',
        },
        {
            'statement': Statement.AsyncFunctionDef,
            'name': 'async_function',
            'category': FunctionType.Coroutine,
            'docstring': 'An asynchronous function.',
            'decorators': [],
            'rtype': 'str',
            'args': 'url: str',
            'kwargs': '',
            'code': 'async def async_function(url: str) -> str:\n    """An asynchronous function."""\n    import aiohttp\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as response:\n            return await response.text()',
        },
        {
            'statement': Statement.FunctionDef,
            'name': 'decorator_function',
            'category': FunctionType.Function,
            'docstring': 'A simple decorator.',
            'decorators': [],
            'rtype': None,
            'args': 'func: Unknown',
            'kwargs': '',
            'code': 'def decorator_function(func):\n    """A simple decorator."""\n\n    def wrapper(*args, **kwargs):\n        print(\'Function is being called\')\n        return func(*args, **kwargs)\n    return wrapper',
        },
        {
            'statement': Statement.FunctionDef,
            'name': 'decorated_function',
            'category': FunctionType.Function,
            'docstring': 'A decorated function.',
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
            'name': 'annotated_function',
            'category': FunctionType.Function,
            'docstring': None,
            'decorators': [],
            'rtype': 'List[int]',
            'args': 'a: int, b: str',
            'kwargs': '',
            'code': 'def annotated_function(a: int, b: str) -> List[int]:\n    return [1, 2, 3]',
        },
        {
            'statement': Statement.FunctionDef,
            'name': 'example_usage_function',
            'category': FunctionType.Function,
            'docstring': 'A function with a docstring example.\n\nExample:\n    result = example_usage_function(1, 2)\n    print(result)  # Outputs 3',
            'decorators': [],
            'rtype': 'int',
            'args': 'a: int, b: int',
            'kwargs': '',
            'code': 'def example_usage_function(a: int, b: int) -> int:\n    """\n    A function with a docstring example.\n\n    Example:\n        result = example_usage_function(1, 2)\n        print(result)  # Outputs 3\n    """\n    return a + b',
        },
        {
            'statement': Statement.FunctionDef,
            'name': 'ellipsis_function',
            'category': FunctionType.Function,
            'docstring': 'A function with an ellipsis.',
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
            'name': '__init__',
            'category': FunctionType.Method,
            'docstring': None,
            'decorators': [],
            'rtype': None,
            'args': 'self: Unknown, value: int',
            'kwargs': '',
            'code': 'def __init__(self, value: int):\n    self.value = value',
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
            'name': 'wrapper',
            'category': FunctionType.Function,
            'docstring': None,
            'decorators': [],
            'rtype': None,
            'args': '',
            'kwargs': '',
            'code': "def wrapper(*args, **kwargs):\n    print('Function is being called')\n    return func(*args, **kwargs)",
        },
    ]

    assert len(statements) == len(expected)

    for i in statements:
        assert i in expected
