from __future__ import annotations

from dataclasses import dataclass
import typing as t


from dew.parser import KwargNode
from dew.utils import get_keyword_seq, get_kwargs
from dew import parse


@dataclass
class Command:
    name: str
    func: t.Callable[..., t.Any | None]
    registry: CommandRegistry

    def command(self, func: t.Callable[..., t.Any | None]):
        self.registry[func.__name__] = Command(func.__name__, func, {})

        return self.registry[func.__name__]


CommandRegistry: t.TypeAlias = dict[str, Command]

Kwargs: t.TypeAlias = list[KwargNode]


@dataclass
class CommandClient:
    di: DI
    registry: CommandRegistry

    def register(self, command: Command):
        self.registry[command.name] = command

    def get_func(
        self, registry: CommandRegistry, command_sequence: list[str]
    ) -> t.Callable | None:
        name = command_sequence.pop(0)

        command = registry.get(name)

        if command is not None:
            if len(command_sequence) != 0:
                return self.get_func(command.registry, [*command_sequence])

            else:
                return command.func
        else:
            raise Exception(f"could not find function for command '{name}'")

    def execute(self, command: str):
        inp = parse(command)

        command_sequence = get_keyword_seq(inp)

        func = self.get_func(self.registry, command_sequence)

        if func is not None:
            kwargs = get_kwargs(inp)

            self.di.set(Kwargs, kwargs)

            decorated_func = self.di.inject(func)

            return decorated_func()

        else:
            raise Exception(f"cannot execute '{command}'")


@dataclass
class DI:
    _data: dict[t.Any, t.Any]

    def set(self, _type: object, value: t.Any):
        existing = self._data.get(_type)

        if existing:
            raise Exception(f"cannot set '{_type}' as dependency, it already exists")

        else:
            self._data[_type] = value

    def inject(
        self, func: t.Callable[..., t.Any | None]
    ) -> t.Callable[..., t.Any | None]:
        def __wrap__(*args, **kwargs):
            __params = {}

            for annot_item in func.__annotations__.items():
                data = self._data.get(annot_item[1])

                if data is not None:
                    __params[annot_item[0]] = self._data[annot_item[1]]

            return func(*args, **__params, **kwargs)

        __wrap__.__name__ = func.__name__

        return __wrap__
