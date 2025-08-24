import typing
from dew import CommandNode, KwargNode


def get_kwargs(node: CommandNode) -> list[KwargNode]:
    tail = node["tail"]

    if isinstance(tail, dict):
        return get_kwargs(tail)

    else:
        return tail


def get_keyword_seq(node: CommandNode) -> list[str]:
    return __get_keyword_seq(node, [node["name"]])


def __get_keyword_seq(node: CommandNode, acc: list[str]) -> list[str]:
    tail = node["tail"]

    if isinstance(tail, dict):
        new_acc = []

        new_acc.extend(acc)
        new_acc.append(tail["name"])

        return __get_keyword_seq(tail, new_acc)

    else:
        return acc


def inspect(
    node: CommandNode, func: typing.Callable[[CommandNode | list[KwargNode]], None]
):
    tail = node["tail"]

    if isinstance(tail, dict):
        func(tail)

        return inspect(tail, func)

    else:
        func(tail)
        return tail
