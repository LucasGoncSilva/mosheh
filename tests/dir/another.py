from tests.example import ExampleTest as ET
from tests.example import create_example_class


class AnotherExampleTest(ET):
    """
    Simple description.

    A way more longer and detailed text with no util stuff for
    pratical reading but extremely relevance for doc testing and
    spending time for those who really cares about reading it.
    """

    def get_constant(self) -> str:
        return self.SOME_CONST

    def custom_create(self) -> None:
        _cls: ET = create_example_class()
        random_str: str = f'{self.get_constant()}{_cls}'

        del random_str


another_instance = AnotherExampleTest()
