import string
import typing


class ParseResult(typing.TypedDict):
    command_name: str

    sub_command_name: str | None

    sub_command_group_name: str | None

    kwargs: list[tuple[str, str]]


class ParserContext:
    def __init__(self, input: str) -> None:
        self.pos = -1
        self.input = input

        self.__peeked = False

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

    def get_remaining_characters(self):
        characters = []

        if self.peek() is not None:
            remaining = self.input[self.pos + 1 :]

            for character in remaining:
                characters.append(character)

            self.__peeked = False

            return characters

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

            if consumed:
                acc = acc + consumed

                return __parse_keyword_recursive(ctx, acc)

            else:
                raise Exception("expected a valid keyword")

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


def parse_kwarg(ctx: ParserContext) -> tuple[str, str]:
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


def parse_kwargs(ctx, acc: list[tuple[str, str]]) -> list[tuple[str, str]]:
    peeked = ctx.peek()

    if peeked:
        return __parse_kwargs_recursive(ctx, acc)

    else:
        raise Exception("expected a character but no characters left")


def __parse_kwargs_recursive(ctx, acc: list[tuple[str, str]]) -> list[tuple[str, str]]:
    peeked = ctx.peek()

    if peeked:
        acc.append(parse_kwarg(ctx))

        escape_whitespaces(ctx)

        return __parse_kwargs_recursive(ctx, acc)

    return acc


def parse_command(ctx: ParserContext) -> ParseResult:
    # try parsing as a command name with subcommand group name with sub command with kwargs

    old_pos = ctx.pos

    try:
        command_name = parse_keyword(ctx)
        escape_whitespaces(ctx)
        sub_command_group_name = parse_keyword(ctx)
        escape_whitespaces(ctx)
        sub_command_name = parse_keyword(ctx)
        escape_whitespaces(ctx)
        kwargs = parse_kwargs(ctx, [])

        if len(ctx.get_remaining_characters()) != 0:
            raise Exception(f"unparsed characters '{ctx.get_remaining_characters()}'")

        return {
            "command_name": command_name,
            "sub_command_name": sub_command_name,
            "sub_command_group_name": sub_command_group_name,
            "kwargs": kwargs,
        }

    except Exception:
        # set back the old pos for other rules to parse

        ctx.pos = old_pos

        pass

    # try parsing as a command name with subcommand group name with sub command (no kwargs)

    old_pos = ctx.pos

    try:
        command_name = parse_keyword(ctx)
        escape_whitespaces(ctx)
        sub_command_group_name = parse_keyword(ctx)
        escape_whitespaces(ctx)
        sub_command_name = parse_keyword(ctx)

        if len(ctx.get_remaining_characters()) != 0:
            raise Exception(f"unparsed characters '{ctx.get_remaining_characters()}'")

        return {
            "command_name": command_name,
            "sub_command_name": sub_command_name,
            "sub_command_group_name": sub_command_group_name,
            "kwargs": [],
        }

    except Exception:
        # set back the old pos for other rules to parse

        ctx.pos = old_pos

        pass

    # try parsing as a command name with subcommand name with kwargs

    old_pos = ctx.pos

    try:
        command_name = parse_keyword(ctx)
        escape_whitespaces(ctx)
        sub_command_name = parse_keyword(ctx)
        escape_whitespaces(ctx)
        kwargs = parse_kwargs(ctx, [])

        if len(ctx.get_remaining_characters()) != 0:
            raise Exception(f"unparsed characters '{ctx.get_remaining_characters()}'")

        return {
            "command_name": command_name,
            "sub_command_name": sub_command_name,
            "sub_command_group_name": None,
            "kwargs": kwargs,
        }

    except Exception:
        # set back the old pos for other rules to parse

        ctx.pos = old_pos

        pass

    # try parsing as a command name with subcommand name (no kwargs)

    old_pos = ctx.pos

    try:
        command_name = parse_keyword(ctx)
        escape_whitespaces(ctx)
        sub_command_name = parse_keyword(ctx)

        if len(ctx.get_remaining_characters()) != 0:
            raise Exception(f"unparsed characters '{ctx.get_remaining_characters()}'")

        return {
            "command_name": command_name,
            "sub_command_name": sub_command_name,
            "sub_command_group_name": None,
            "kwargs": [],
        }

    except Exception:
        # set back the old pos for other rules to parse

        ctx.pos = old_pos

        pass

    # try parsing as a command name with kwargs

    old_pos = ctx.pos

    try:
        command_name = parse_keyword(ctx)
        escape_whitespaces(ctx)
        kwargs = parse_kwargs(ctx, [])

        if len(ctx.get_remaining_characters()) != 0:
            raise Exception(f"unparsed characters '{ctx.get_remaining_characters()}'")

        return {
            "command_name": command_name,
            "sub_command_name": None,
            "sub_command_group_name": None,
            "kwargs": kwargs,
        }

    except Exception:
        # set back the old pos for other rules to parse

        ctx.pos = old_pos

        pass

    # try parsing as a command name only

    old_pos = ctx.pos

    try:
        command_name = parse_keyword(ctx)

        if len(ctx.get_remaining_characters()) != 0:
            raise Exception(f"unparsed characters '{ctx.get_remaining_characters()}'")

        return {
            "command_name": command_name,
            "sub_command_name": None,
            "sub_command_group_name": None,
            "kwargs": [],
        }

    except Exception:
        raise Exception(f"could not parse '{ctx.input}'")


def parse(cmd: str):
    ctx = ParserContext(input=cmd)

    result = parse_command(ctx)

    return result
