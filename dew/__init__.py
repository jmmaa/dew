import itertools
import string
import typing
import dataclasses
import typing


whitespace_chars = [" ", "\t", "\r"]


class ParseResult(typing.TypedDict):

    command_name: str

    sub_command_name: str | None

    sub_command_group_name: str | None

    kwargs: list[tuple[str, str]]



@dataclasses.dataclass
class ParserContext:
    chars: typing.Iterator[str]

    def peek(self):
        try:
            peeked = next(self.chars)
            self.chars = itertools.chain([peeked], self.chars)

            return peeked

        except StopIteration:
            return None

    def consume(self):

        consumed = next(self.chars)

        return consumed


    def escape_whitespaces(self):
        peeked = self.peek()

        if peeked:
            if peeked in whitespace_chars:
                self.consume()

                self.escape_whitespaces()

    def parse_keyword(self, acc: str = "") -> str:
        peeked = self.peek()

        if peeked:
            if peeked in string.ascii_letters + "_":
                consumed = self.consume()

                if consumed:
                    acc = acc + consumed

                    return self.__parse_keyword_recursive(acc)

                else:
                    raise Exception("expected a valid keyword")

            else:
                raise Exception(
                    f"invalid character '{peeked}' cannot construct a valid keyword"
                )

        else:
            raise Exception("no characters left to construct a keyword")

    def __parse_keyword_recursive(self, acc: str = "") -> str:
        peeked = self.peek()

        if peeked:
            if peeked in string.ascii_letters + string.digits + "_":
                consumed = self.consume()

                if consumed:
                    acc = acc + consumed

                    return self.__parse_keyword_recursive(acc)

        return acc

    def parse_value(self, acc: str = "") -> str:
        peeked = self.peek()

        if peeked:
            if peeked in string.ascii_letters + string.digits + "_":
                consumed = self.consume()

                acc = acc + consumed

                return self.__parse_value_recursive(acc)


            # for handling quoted inputs
            if peeked == "\"":
                consumed = self.consume() # escape quote

                return self.__parse_quoted_value_recursive(acc)

            else:
                raise Exception(
                    f"invalid character '{peeked}' cannot construct a valid value"
                )

        else:
            raise Exception("no characters left to construct a valid value")

    def __parse_quoted_value_recursive(self, acc: str = "") -> str:
        peeked = self.peek()

        if peeked:
            if peeked != '"':
                consumed = self.consume()


                acc = acc + consumed

                return self.__parse_quoted_value_recursive(acc)

            else:
                consumed = self.consume() # escape quote

                return acc


        raise Exception("expected a '\"'")

    def __parse_value_recursive(self, acc: str = "") -> str:
        peeked = self.peek()

        if peeked:
            if peeked in string.ascii_letters + string.digits + "_":
                consumed = self.consume()

                if consumed:
                    acc = acc + consumed

                    return self.__parse_value_recursive(acc)

        return acc

    def parse_kwarg(self) -> tuple[str, str]:
        keyword = self.parse_keyword()

        self.escape_whitespaces()

        peeked = self.peek()

        if peeked:
            if peeked == ":":
                self.consume()  # escape colon

                self.escape_whitespaces()

                value = self.parse_value()

                return keyword, value

            else:
                raise Exception(f"expected ':' but found '{peeked}'")
        else:
            raise Exception("expected ':' but no characters left")

    def parse_kwargs(self, acc: list[tuple[str, str]] = []) -> list[tuple[str, str]]:
        peeked = self.peek()

        if peeked:
            return self.__parse_kwargs_recursive(acc)

        else:
            raise Exception("expected a character but no characters left")

    def __parse_kwargs_recursive(
        self, acc: list[tuple[str, str]] = []
    ) -> list[tuple[str, str]]:
        peeked = self.peek()

        if peeked:
            acc.append(self.parse_kwarg())

            self.escape_whitespaces()

            return self.__parse_kwargs_recursive(acc)

        return acc

    def parse_command_name(self, acc: str = "") -> str:
        return self.parse_keyword(acc)

    def parse_sub_command_name(self, acc: str = "") -> str:
        return self.parse_keyword(acc)

    def parse_sub_command_group_name(self, acc: str = "") -> str:
        return self.parse_keyword(acc)


    def parse_command(self) -> ParseResult:
        # try parsing as command

        old, to_parse = itertools.tee(self.chars)
        try:
            self.chars = to_parse

            command_name = self.parse_command_name()

            self.escape_whitespaces()

            kwargs = self.parse_kwargs()

            return {
                "command_name": command_name,
                "sub_command_name": None,
                "sub_command_group_name": None,
                "kwargs": kwargs,
            }

        except Exception:
            pass

        # try parsing as subcommand

        self.chars = old
        old, to_parse = itertools.tee(self.chars)

        try:
            self.chars = to_parse

            command_name = self.parse_command_name()

            self.escape_whitespaces()

            subcommand_name = self.parse_sub_command_name()

            self.escape_whitespaces()

            kwargs = self.parse_kwargs()

            return {
                "command_name": command_name,
                "sub_command_name": subcommand_name,
                "sub_command_group_name": None,
                "kwargs": kwargs,
            }

        except Exception as e:
            pass

        self.chars = old
        old, to_parse = itertools.tee(self.chars)

        # try parsing as subcommand group
        try:
            self.chars = to_parse

            command_name = self.parse_command_name()

            self.escape_whitespaces()

            subcommand_group_name = self.parse_sub_command_group_name()

            self.escape_whitespaces()

            subcommand_name = self.parse_sub_command_name()

            self.escape_whitespaces()

            kwargs = self.parse_kwargs()

            return {
                "command_name": command_name,
                "sub_command_name": subcommand_name,
                "sub_command_group_name": subcommand_group_name,
                "kwargs": kwargs,
            }

        except Exception as e:
            raise e



def parse(input: str):

    chars = iter(input)

    parser_context = ParserContext(chars)

    result = parser_context.parse_command()

    return result