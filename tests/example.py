import string
from abc import ABC
from math import sin, sqrt


CONSTANT: str = string.ascii_letters[:10]
NUMBER: int = int(sin(1) * sqrt(25))


class ExampleTest(ABC):
    SOME_CONST: str = 'Random String'

    def __init__(self, num: int) -> None:
        self.value: str = CONSTANT * num


def create_example_class() -> ExampleTest:
    _cls: ExampleTest = ExampleTest(NUMBER)

    return _cls


def another_func(instances: list[ExampleTest]) -> int:
    return len(instances)


instance: ExampleTest = create_example_class()

num_of_instances: int = another_func([instance, create_example_class()])

assert num_of_instances == 2
