from dew import CommandNode, KwargNodes


def get_kwargs(node: CommandNode) -> KwargNodes:
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
        return __get_keyword_seq(tail, [*acc, tail["name"]])

    else:
        return acc
