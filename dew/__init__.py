import itertools
import string
import typing
import dataclasses


T = typing.TypeVar("T")


whitespace_chars = [" ", "\t", "\r"]


@dataclasses.dataclass
class Parser:
    chars: typing.Iterator[str]

    def peek(self):
        try:
            peeked = next(self.chars)

            self.chars = itertools.chain([peeked], self.chars)

            return peeked

        except StopIteration:
            return None

    def consume(self):
        try:
            consumed = next(self.chars)

            return consumed

        except StopIteration:
            return None

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

                if consumed:
                    acc = acc + consumed

                    return self.__parse_value_recursive(acc)

                else:
                    raise Exception("expected a valid value")

            else:
                raise Exception(
                    f"invalid character '{peeked}' cannot construct a valid value"
                )

        else:
            raise Exception("no characters left to construct a valid value")

    def __parse_value_recursive(self, acc: str = "") -> str:
        peeked = self.peek()

        if peeked:
            if peeked in string.ascii_letters + string.digits + "_":
                consumed = self.consume()

                if consumed:
                    acc = acc + consumed

                    return self.__parse_keyword_recursive(acc)

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

    def parse_subcommand_name(self, acc: str = "") -> str:
        return self.parse_keyword(acc)

    def parse_subcommand_group_name(self, acc: str = "") -> str:
        return self.parse_keyword(acc)

    def parse_subcommand_group(self) -> dict:
        subcommand_group_name = self.parse_subcommand_name()

        self.escape_whitespaces()

        subcommand_name = self.parse_subcommand_name()

        self.escape_whitespaces()

        kwargs = self.parse_kwargs()

        return {
            "name": subcommand_group_name,
            "subcommand": subcommand_name,
            "kwargs": kwargs,
        }

    def parse_command(self) -> dict:
        # try parsing as command

        old, to_parse = itertools.tee(self.chars)
        try:
            self.chars = to_parse

            command_name = self.parse_command_name()

            self.escape_whitespaces()

            kwargs = self.parse_kwargs()

            return {
                "command_name": command_name,
                "subcommand_group_name": None,
                "subcommand_name": None,
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

            subcommand_name = self.parse_subcommand_name()

            self.escape_whitespaces()

            kwargs = self.parse_kwargs()

            return {
                "command_name": command_name,
                "subcommand_group_name": None,
                "subcommand_name": subcommand_name,
                "kwargs": kwargs,
            }

        except Exception as e:
            print(list(self.chars))
            print("from sub command parser: ", e)
            pass

        self.chars = old
        old, to_parse = itertools.tee(self.chars)

        # try parsing as subcommand group
        try:
            self.chars = to_parse

            command_name = self.parse_command_name()

            self.escape_whitespaces()

            subcommand_group = self.parse_subcommand_group()

            return {"command": {"name": command_name, "sub_command": subcommand_group}}

        except Exception as e:
            raise e
