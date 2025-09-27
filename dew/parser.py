from __future__ import annotations
import string

import typing_extensions as t

from dew.types import CommandNode, KwargNode, KwargNodes

WHITESPACES: t.Final[str] = " \t\r"

VALID_KEYWORD_FIRST_CHARACTERS: t.Final[str] = string.ascii_letters + "_" + "-"


VALID_KEYWORD_BODY_CHARACTERS: t.Final[str] = string.ascii_letters + string.digits + "_" + "-"

VALID_UNQUOTED_VALUE_BODY_CHARACTERS: t.Final[str] = (
    string.ascii_letters + string.digits + string.punctuation
)

VALID_QUOTED_VALUE_BODY_CHARACTERS: t.Final[str] = (
    VALID_UNQUOTED_VALUE_BODY_CHARACTERS + WHITESPACES
)


class ParserContext:
    """The context of the parser"""

    def __init__(self, input: str) -> None:
        self.pos = -1
        self.input = input

        self.__peeked = False

    def peek(self) -> str | None:
        try:
            self.__peeked = True

            return self.input[self.pos + 1]

        except IndexError:
            return None

    def consume(self) -> str:
        if self.__peeked:  # need to peek first before consuming or else raise an error
            self.pos += 1

            self.__peeked = False

            return self.input[self.pos]

        raise Exception("consumed an unpeeked character")

    def get_remaining_characters(self):
        if self.peek() is not None:
            remaining = self.input[self.pos + 1 :]

            self.__peeked = False

            return remaining

        else:
            return []


def escape_whitespaces(ctx: ParserContext):
    peeked = ctx.peek()

    if peeked:
        if peeked in WHITESPACES:
            ctx.consume()

            escape_whitespaces(ctx)


def parse_keyword(ctx: ParserContext, acc: str = "") -> str:
    peeked = ctx.peek()

    if peeked:
        if peeked in VALID_KEYWORD_FIRST_CHARACTERS:
            return __parse_keyword_recursive(ctx, acc)

        else:
            raise Exception(
                f"invalid character '{peeked}' cannot construct a valid keyword"
            )

    else:
        raise Exception("no characters left to construct a keyword")


def __parse_keyword_recursive(ctx: ParserContext, acc: str = "") -> str:
    peeked = ctx.peek()
    if peeked:
        if peeked in VALID_KEYWORD_BODY_CHARACTERS:
            consumed = ctx.consume()

            acc = acc + consumed

            return __parse_keyword_recursive(ctx, acc)

    return acc


def parse_value(ctx: ParserContext, acc: str = "") -> str:
    peeked = ctx.peek()

    if peeked:
        # for handling quoted inputs
        if peeked == '"':
            ctx.consume()  # escape quote

            return __parse_double_quoted_value_recursive(ctx, acc)

        elif peeked == "'":
            ctx.consume()  # escape quote

            return __parse_single_quoted_value_recursive(ctx, acc)

        elif peeked in VALID_UNQUOTED_VALUE_BODY_CHARACTERS:
            return __parse_value_recursive(ctx, acc)

        else:
            raise Exception(
                f"invalid character '{peeked}' cannot construct a valid value"
            )

    else:
        raise Exception("no characters left to construct a valid value")


def __parse_value_recursive(ctx: ParserContext, acc: str = "") -> str:
    peeked = ctx.peek()

    if peeked:
        if peeked in VALID_UNQUOTED_VALUE_BODY_CHARACTERS:
            consumed = ctx.consume()

            if consumed:
                acc = acc + consumed

                return __parse_value_recursive(ctx, acc)

    return acc


def __parse_double_quoted_value_recursive(ctx: ParserContext, acc: str = "") -> str:
    peeked = ctx.peek()

    if peeked:
        if peeked == "\\":
            ctx.consume()  # escape backward slash

            escaped = ctx.peek()

            if escaped:
                print("ESCAPED!:", escaped)
                consumed = ctx.consume()  # escape character

                acc = acc + consumed

                return __parse_double_quoted_value_recursive(ctx, acc)

            else:
                raise Exception("expected an escape character")
        elif peeked != '"':
            consumed = ctx.consume()

            acc = acc + consumed

            return __parse_double_quoted_value_recursive(ctx, acc)

        elif peeked == '"':
            ctx.consume()  # escape quote

            return acc

        else:
            raise Exception('expected a character or """')

    raise Exception('expected a """')


def __parse_single_quoted_value_recursive(ctx: ParserContext, acc: str = "") -> str:
    peeked = ctx.peek()

    if peeked:
        if peeked == "\\":
            ctx.consume()  # escape backward slash

            escaped = ctx.peek()

            if escaped:
                print("ESCAPED!:", escaped)
                consumed = ctx.consume()  # escape character

                acc = acc + consumed

                return __parse_single_quoted_value_recursive(ctx, acc)

            else:
                raise Exception("expected an escape character")

        elif peeked != "'":
            consumed = ctx.consume()

            acc = acc + consumed

            return __parse_single_quoted_value_recursive(ctx, acc)

        elif peeked == "'":
            ctx.consume()  # escape quote

            return acc

        else:
            raise Exception('expected a character or "\'"')

    raise Exception('expected a "\'"')


def parse_kwarg(ctx: ParserContext) -> "KwargNode":
    keyword = parse_keyword(ctx)

    escape_whitespaces(ctx)

    peeked = ctx.peek()

    if peeked:
        if peeked == ":":
            ctx.consume()  # escape colon

            escape_whitespaces(ctx)

            value = parse_value(ctx)

            return keyword, value

        else:
            raise Exception(f"expected ':' but found '{peeked}'")
    else:
        raise Exception("expected ':' but no characters left")


def parse_kwargs(ctx, acc: KwargNodes) -> "KwargNodes":
    peeked = ctx.peek()

    if peeked:
        return __parse_kwargs_recursive(ctx, acc)

    else:
        raise Exception("expected a character but no characters left")


def __parse_kwargs_recursive(ctx, acc: KwargNodes) -> KwargNodes:
    peeked = ctx.peek()

    if peeked:
        acc.append(parse_kwarg(ctx))

        escape_whitespaces(ctx)

        return __parse_kwargs_recursive(ctx, acc)

    return acc


def check_unparsed(ctx):
    if len(ctx.get_remaining_characters()) != 0:
        raise Exception(f"unparsed characters '{ctx.get_remaining_characters()}'")


def parse_command(ctx: ParserContext) -> CommandNode:
    # try parsing as a command name with subcommand

    old_pos = ctx.pos

    try:
        keyword = parse_keyword(ctx)

        escape_whitespaces(ctx)

        command = parse_command(ctx)

        check_unparsed(ctx)

        return {"name": keyword, "tail": command}

    except Exception:
        ctx.pos = old_pos

    # try parsing as a command name with kwargs

    try:
        keyword = parse_keyword(ctx)

        escape_whitespaces(ctx)

        kwargs = parse_kwargs(ctx, [])

        check_unparsed(ctx)

        return {"name": keyword, "tail": kwargs}

    except Exception:
        ctx.pos = old_pos

    # try parsing as a command name only
    try:
        keyword = parse_keyword(ctx)

        check_unparsed(ctx)

        return {"name": keyword, "tail": []}

    except Exception:
        ctx.pos = old_pos

        raise Exception(f"failed parsing command '{ctx.get_remaining_characters()}'")


def parse(input: str):
    ctx = ParserContext(input=input)

    result = parse_command(ctx)

    return result
