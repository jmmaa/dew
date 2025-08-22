from __future__ import annotations


import string
import typing

Kwarg: typing.TypeAlias = tuple[str, str]


class Command(typing.TypedDict):
    name: str
    tail: Command | list[Kwarg]


class ParserContext:
    def __init__(self, input: str) -> None:
        self.pos = -1
        self.input = input

        self.__peeked = False
        self.__checkpoint = 0

    def peek(self):
        try:
            self.__peeked = True

            return self.input[self.pos + 1]

        except Exception:
            return None

    def consume(self):
        if self.__peeked:  # need to peek first before consuming
            self.pos += 1

            self.__peeked = False

            return self.input[self.pos]

        raise Exception("consumed an unpeeked character")

    def set_checkpoint(self):
        self.__checkpoint = self.pos

    def get_remaining_string(self):
        if self.peek() is not None:
            remaining = self.input[self.pos + 1 :]

            self.__peeked = False

            return remaining

        else:
            return []


whitespace_chars = [" "]


def escape_whitespaces(ctx: ParserContext):
    peeked = ctx.peek()

    if peeked:
        if peeked in whitespace_chars:
            ctx.consume()

            escape_whitespaces(ctx)


def parse_keyword(ctx: ParserContext, acc: str = "") -> str:
    peeked = ctx.peek()

    if peeked:
        if peeked in string.ascii_letters + "_":
            consumed = ctx.consume()

            acc = acc + consumed

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
        if peeked in string.ascii_letters + string.digits + "_":
            consumed = ctx.consume()

            if consumed:
                acc = acc + consumed

                return __parse_keyword_recursive(ctx, acc)

    return acc


def parse_value(ctx: ParserContext, acc: str = "") -> str:
    peeked = ctx.peek()

    if peeked:
        if peeked in string.ascii_letters + string.digits + "_":
            consumed = ctx.consume()

            acc = acc + consumed

            return __parse_value_recursive(ctx, acc)

        # for handling quoted inputs
        if peeked == '"':
            consumed = ctx.consume()  # escape quote

            return __parse_quoted_value_recursive(ctx, acc)

        else:
            raise Exception(
                f"invalid character '{peeked}' cannot construct a valid value"
            )

    else:
        raise Exception("no characters left to construct a valid value")


def __parse_value_recursive(ctx: ParserContext, acc: str = "") -> str:
    peeked = ctx.peek()

    if peeked:
        if peeked in string.ascii_letters + string.digits + "_":
            consumed = ctx.consume()

            if consumed:
                acc = acc + consumed

                return __parse_value_recursive(ctx, acc)

    return acc


def __parse_quoted_value_recursive(ctx: ParserContext, acc: str = "") -> str:
    peeked = ctx.peek()

    if peeked:
        if peeked != '"':
            consumed = ctx.consume()

            acc = acc + consumed

            return __parse_quoted_value_recursive(ctx, acc)

        else:
            consumed = ctx.consume()  # escape quote

            return acc

    raise Exception("expected a '\"'")


def parse_kwarg(ctx: ParserContext) -> Kwarg:
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


def parse_kwargs(ctx, acc: list[tuple[str, str]]) -> list[Kwarg]:
    peeked = ctx.peek()

    if peeked:
        return __parse_kwargs_recursive(ctx, acc)

    else:
        raise Exception("expected a character but no characters left")


def __parse_kwargs_recursive(ctx, acc: list[tuple[str, str]]) -> list[Kwarg]:
    peeked = ctx.peek()

    if peeked:
        acc.append(parse_kwarg(ctx))

        escape_whitespaces(ctx)

        return __parse_kwargs_recursive(ctx, acc)

    return acc


def check_unparsed(ctx):
    if len(ctx.get_remaining_string()) != 0:
        raise Exception(f"unparsed characters '{ctx.get_remaining_string()}'")


def parse_command(ctx) -> Command:
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

        raise Exception(f"failed parsing command '{ctx.get_remaining_string()}'")


def parse(input: str):
    ctx = ParserContext(input=input)

    result = parse_command(ctx)

    return result
