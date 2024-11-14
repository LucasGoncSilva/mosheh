import string
from abc import ABC
from math import sin, sqrt


CONSTANT: str = string.ascii_letters[:10]
NUMBER: int = int(sin(1) * sqrt(25))


class ExampleTest(ABC):
    """
    Simple description.

    A way more longer and detailed text with no util stuff for
    pratical reading but extremely relevance for doc testing and
    spending time for those who really cares about reading it.
    """

    SOME_CONST: str = 'Random String'

    def __init__(self, num: int) -> None:
        self.value: str = CONSTANT * num


def create_example_class(num: int = NUMBER) -> ExampleTest:
    """
    Simple description.

    A way more longer and detailed text with no util stuff for
    pratical reading but extremely relevance for doc testing and
    spending time for those who really cares about reading it.

    :param num: an int for dealing random stuff.
    :type num: int, optional.
    :return: ExampleTest instance.
    :rtype: ExampleTest

    :Example:
    >>> create_example_class()
    <class 'ExampleTest'>
    """

    _cls: ExampleTest = ExampleTest(num)

    return _cls


def another_func(instances: list[ExampleTest]) -> int:
    """
    Simple description.

    A way more longer and detailed text with no util stuff for
    pratical reading but extremely relevance for doc testing and
    spending time for those who really cares about reading it.

    :param instances: list of ExampleTest instances.
    :type instances: list[ExampleTest].
    :return: a number.
    :rtype: int

    :Example:
    >>> another_func([create_example_class()])
    1
    """

    return len(instances)


instance: ExampleTest = create_example_class()

num_of_instances: int = another_func([instance, create_example_class()])

assert num_of_instances == 2
