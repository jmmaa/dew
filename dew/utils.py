import typing
from dew import Command, Kwarg


def get_kwargs(command: Command) -> list[Kwarg]:
    tail = command["tail"]

    if isinstance(tail, dict):
        return get_kwargs(tail)

    else:
        return tail


def inspect(command: Command, func: typing.Callable[[Command | list[Kwarg]], None]):
    tail = command["tail"]

    if isinstance(tail, dict):
        func(tail)

        return inspect(tail, func)

    else:
        func(tail)
        return tail
