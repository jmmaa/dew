from __future__ import annotations
import typing as t


KwargNode: t.TypeAlias = tuple[str, str]
"""
The keyword argument node of the syntax tree

a tuple where the 1st value is
the keyword and the second is the value

"""

KwargNodes: t.TypeAlias = list[KwargNode]
"""list of keyword argument nodes"""


class CommandNode(t.TypedDict):
    """The command node of the syntax tree"""

    name: str
    """name of the command node"""

    tail: CommandNode | KwargNodes
    """
    the subsequent node of the current command 
    it can either be a :py:`CommandNode` or :py:`KwargNodes`
    """
