from tests.example import ExampleTest, create_example_class


class AnotherExampleTest(ExampleTest):
    def def_constant(self) -> str:
        return self.SOME_CONST

    def custom_create(self) -> None:
        _cls: ExampleTest = create_example_class()
