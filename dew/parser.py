# MIT License
#
# Copyright (c) 2025 jma
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Parser implementation."""

from __future__ import annotations

import string
from dataclasses import dataclass

import typing_extensions as t

WHITESPACES: t.Final[str] = " \t\r\n"
ASSIGNMENT_OPERATOR: t.Final[str] = "="
ESCAPE_CHARACTER: t.Final[str] = "\\"
DOUBLE_QUOTES: t.Final[str] = '"'
SINGLE_QUOTE: t.Final[str] = "'"

PARTIAL_PUNCTUATION: t.Final[str] = (
    string.punctuation.replace(ASSIGNMENT_OPERATOR, "")
    .replace(ESCAPE_CHARACTER, "")
    .replace(DOUBLE_QUOTES, "")
    .replace(SINGLE_QUOTE, "")
)

LETTERS: t.Final[str] = string.ascii_letters
NUMBERS: t.Final[str] = string.digits

VALID_VALUE_CHARACTERS: t.Final[str] = LETTERS + NUMBERS + PARTIAL_PUNCTUATION

ANY_CHARACTER: t.Final[str] = (
    VALID_VALUE_CHARACTERS
    + DOUBLE_QUOTES
    + SINGLE_QUOTE
    + ASSIGNMENT_OPERATOR
    + ESCAPE_CHARACTER
)


VALID_UNQUOTED_VALUE_CHARACTERS: t.Final[str] = (
    VALID_VALUE_CHARACTERS + ESCAPE_CHARACTER
)

VALID_DOUBLE_QUOTED_VALUE_CHARACTERS: t.Final[str] = (
    VALID_VALUE_CHARACTERS + ASSIGNMENT_OPERATOR + SINGLE_QUOTE + ESCAPE_CHARACTER
)


T = t.TypeVar("T")

TokenType: t.TypeAlias = t.Literal["WHITESPACES", "VALUE", "ASSIGN_OP"]

Token: t.TypeAlias = tuple[TokenType, str]


class Command(t.TypedDict):
    """The `dict` representation of the command data."""

    args: list[str]
    """
    The positional arguments of the command.
    """

    kwargs: list[tuple[str, str]]
    """
    The keyword arguments of the command.
    """


class DewStr(str):
    """A class that subclasses `str`.

    This provides necessary methods for parsing logic.
    """

    def __new__(cls, *args, **kwargs):
        """A constructor method, used to construct immutable class `str`."""
        cls.pos = -1
        cls.__peeked = False

        return str.__new__(cls, *args, **kwargs)

    def peek(self) -> str | None:
        """Peeks the current character to focus on processing.

        Note:
            This has to be called first before `DewStr.consume()` or else it will throw
            an `Exception`. This is to prevent consuming characters that may eventually
            cause an `IndexError`

        Returns:
            str | None: The peeked character, `None` if already in end of file.
        """
        try:
            self.__peeked = True

            return self[self.pos + 1]

        except IndexError:
            return None

    def consume(self) -> str:
        """Consumes a character.

        Returns:
            str: The consumed character.

        Raises:
            Exception: raised when this method is used without calling `DewStr.peek()` first.
        """
        if self.__peeked:  # need to peek first before consuming or else raise an error
            self.pos += 1
            self.__peeked = False

            return self[self.pos]

        raise Exception("consumed an unpeeked character")

    def get_remaining_string(self) -> str:
        """Gets the remaining string to peek/consume.

        Returns:
            str: The remaining string, if theres no string left, it will return an empty string asdasdsaddasdasdadadadasdadad
        """
        if self.peek() is not None:
            remaining = self[self.pos + 1 :]

            self.__peeked = False

            return remaining

        else:
            return ""


@dataclass
class Tokenizer:
    """The tokenizer class for converting input string to tokens.

    Attributes:
        input (DewStr): A custom string derived from `DewStr` class.
    """

    input: DewStr

    def __escape(self):
        self.input.consume()  # skip the escape character
        peeked = self.input.peek()

        if peeked:
            return self.input.consume()

        else:
            raise Exception(f"expected a character to escape, found '{peeked}'")

    def __tokenize_whitespace(self):
        peeked = self.input.peek()

        whitespaces = str()

        while peeked is not None:
            if peeked in WHITESPACES:
                whitespaces += self.input.consume()

            else:
                break

            peeked = self.input.peek()

        return "WHITESPACES", whitespaces

    def __tokenize_unquoted_value(self):
        peeked = self.input.peek()

        unquoted_value_characters = str()
        while peeked is not None:
            if peeked in VALID_VALUE_CHARACTERS:
                unquoted_value_characters += self.input.consume()

            elif peeked == ESCAPE_CHARACTER:
                unquoted_value_characters += self.__escape()

            else:
                break

            peeked = self.input.peek()
        return "VALUE", unquoted_value_characters

    def __tokenize_double_quoted_value(self):
        self.input.consume()  # escape the starting quotes

        peeked = self.input.peek()
        double_quoted_value_characters = str()

        while peeked is not None:
            if peeked == DOUBLE_QUOTES:
                self.input.consume()  # escape the ending quotes
                break

            elif peeked in (
                VALID_VALUE_CHARACTERS
                + ASSIGNMENT_OPERATOR
                + SINGLE_QUOTE
                + WHITESPACES
            ):
                double_quoted_value_characters += self.input.consume()

            elif peeked == ESCAPE_CHARACTER:
                double_quoted_value_characters += self.__escape()

            else:
                raise Exception(f"unknown character '{peeked}'")

            peeked = self.input.peek()

        return "VALUE", double_quoted_value_characters

    def __tokenize_single_quoted_value(self):
        self.input.consume()  # escape the quotes

        peeked = self.input.peek()
        single_quoted_value_characters = str()

        while peeked is not None:
            if peeked == SINGLE_QUOTE:
                self.input.consume()  # escape the quotes
                break

            elif peeked in (
                VALID_VALUE_CHARACTERS
                + ASSIGNMENT_OPERATOR
                + SINGLE_QUOTE
                + WHITESPACES
            ):
                single_quoted_value_characters += self.input.consume()

            elif peeked == ESCAPE_CHARACTER:
                single_quoted_value_characters += self.__escape()

            else:
                raise Exception(f"unknown character '{peeked}'")

        return "VALUE", single_quoted_value_characters

    def __tokenize_assignment_operator(self):
        value = self.input.consume()

        return "ASSIGN_OP", value

    def tokenize(self) -> list[Token]:
        """The tokenizer class for converting input string to tokens.

        Returns:
            list[str]: List of `Token`.
        """
        tokens: list[Token]
        tokens = []

        peeked = self.input.peek()
        while peeked is not None:
            if peeked in WHITESPACES:
                tokens.append(self.__tokenize_whitespace())

            elif peeked in VALID_UNQUOTED_VALUE_CHARACTERS:
                tokens.append(self.__tokenize_unquoted_value())

            elif peeked == DOUBLE_QUOTES:
                tokens.append(self.__tokenize_double_quoted_value())

            elif peeked == SINGLE_QUOTE:
                tokens.append(self.__tokenize_single_quoted_value())

            elif peeked == ASSIGNMENT_OPERATOR:
                tokens.append(self.__tokenize_assignment_operator())

            else:
                raise Exception(f"unknown character '{peeked}'")

            peeked = self.input.peek()

        return tokens


@dataclass
class Parser:
    """The Parser class for converting list of tokens into `Command`.

    Attributes:
        tokens (list[Token]): list of tokens.
    """

    tokens: list[Token]

    def __peek_token(self):
        try:
            return self.tokens[0]
        except IndexError:
            return None

    def __consume_token(self):
        return self.tokens.pop(0)

    def __escape_whitespace(self) -> None:
        peeked = self.__peek_token()

        if peeked:
            if peeked[0] == "WHITESPACES":
                self.__consume_token()

    def __check_unparsed(self):
        if len(self.tokens) != 0:
            raise Exception(f"unparsed tokens: {self.tokens}")

    def __parse_arg(self) -> str:
        peeked = self.__peek_token()

        if peeked:
            if peeked[0] == "VALUE":
                token = self.__consume_token()

                return token[1]

            else:
                raise Exception(f"expected value token, found {peeked}")
        else:
            raise Exception("expected value token, found None")

    def __parse_args(self) -> list[str]:
        return self.__recursive_parse_args([])

    def __recursive_parse_args(self, acc: list[str]):
        peeked = self.__peek_token()

        if peeked:
            tokens = self.tokens.copy()
            if peeked[0] == "VALUE":
                new_acc = [*acc, self.__parse_arg()]
                self.__escape_whitespace()

                peeked = self.__peek_token()

                if peeked:
                    if peeked[0] == "VALUE":
                        return self.__recursive_parse_args(new_acc)

                    elif peeked[0] == "ASSIGN_OP":
                        self.tokens = tokens
                        return acc

                    else:
                        raise Exception(f"unknown token error: {peeked}")

                else:
                    return new_acc
            else:
                return acc
        else:
            return acc

    def __parse_assign_op(self):
        peeked = self.__peek_token()

        if peeked:
            if peeked[0] == "ASSIGN_OP":
                self.__consume_token()

                self.__escape_whitespace()

            else:
                raise Exception(f"expected a assign_operator token, found {peeked}")
        else:
            raise Exception("expected a assign_operator token, found None")

    def __parse_kwarg(self):
        peeked = self.__peek_token()

        if peeked:
            if peeked[0] == "VALUE":
                kwarg_name = self.__parse_arg()

                self.__escape_whitespace()
                self.__parse_assign_op()
                self.__escape_whitespace()

                kwarg_value = self.__parse_arg()

                return kwarg_name, kwarg_value

            else:
                raise Exception(f"expected value token, found {peeked}")
        else:
            raise Exception("expected value token, found None")

    def __parse_kwargs(self):
        return self.__recursive_parse_kwargs([])

    def __recursive_parse_kwargs(self, acc: list[tuple[str, str]]):
        peeked = self.__peek_token()

        if peeked:
            if peeked[0] == "VALUE":
                acc = [*acc, self.__parse_kwarg()]

                self.__escape_whitespace()
                return self.__recursive_parse_kwargs(acc)

            else:
                raise Exception(f"unknown token error: {peeked}")
        else:
            return acc

    def parse(self) -> Command:
        """Parses the tokens into `Command`.

        Returns:
            `Command`: The parsed command data.
        """
        args = self.__parse_args()
        self.__escape_whitespace()
        kwargs = self.__parse_kwargs()
        self.__check_unparsed()

        return {"args": args, "kwargs": kwargs}


def parse(input: str):
    """Parses the dew command language into `Command`.

    Returns:
        Command: The parsed command data.
    """
    string = DewStr(input)

    tokens = Tokenizer(string).tokenize()

    result = Parser(tokens).parse()

    return result
