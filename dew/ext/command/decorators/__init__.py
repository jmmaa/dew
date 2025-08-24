from dew.ext.command import Command

import typing as t


def command(func: t.Callable[..., t.Any | None]) -> Command:
    return Command(func.__name__, func, {})


def name(
    _name: str,
) -> t.Callable[
    [t.Callable[..., t.Any | None]],
    t.Callable[..., t.Any | None],
]:
    def __wrapper__(func: t.Callable[..., t.Any | None]):
        func.__name__ = _name

        return func

    return __wrapper__
