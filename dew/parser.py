# ruff: noqa: D100

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


class StringError(Exception):
    """Error Class for string-related errors."""


class TokenizerError(Exception):
    """Error Class for tokenization-related errors."""


class ParserError(Exception):
    """Error Class for parsing-related errors."""


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


@dataclass
class Tokenizer:
    """The tokenizer class for converting input string to tokens.

    Attributes:
        input (DewStr): A custom string derived from `DewStr` class.
    """

    input: str

    pos: int = -1

    _peeked: bool = False

    def peek(self) -> str | None:
        """Peeks the current character to focus on processing.

        Note:
            This has to be called first before `DewStr.consume()` or
            else it will throw an `Exception`. This is to prevent
            consuming characters that may eventually cause an
            `IndexError`

        Returns:
            str | None: The peeked character, `None` if already in end
            of file.
        """
        try:
            self._peeked = True

            return self.input[self.pos + 1]

        except IndexError:
            return None

    def consume(self) -> str:
        """Consumes a character.

        Returns:
            str: The consumed character.

        Raises:
            Exception: raised when this method is used without calling
            `DewStr.peek()` first.
        """
        if self._peeked:  # need to peek first before consuming or else raise an error
            self.pos += 1
            self._peeked = False

            return self.input[self.pos]

        err = "consumed an unpeeked character"

        raise StringError(err)

    def get_remaining_string(self) -> str:
        """Gets the remaining string to peek/consume.

        Returns:
            str: The remaining string, if theres no string left, it will
            return an empty string.
        """
        if self.peek() is not None:
            remaining = self.input[self.pos + 1 :]

            self._peeked = False

            return remaining

        return ""

    def __escape(self) -> str:
        self.consume()  # skip the escape character
        peeked = self.peek()

        if peeked:
            return self.consume()

        err = f"expected a character to escape, found '{peeked}'"

        raise TokenizerError(err)

    def __tokenize_whitespace(self) -> Token:
        peeked = self.peek()

        whitespaces = ""

        while peeked is not None:
            if peeked in WHITESPACES:
                whitespaces += self.consume()

            else:
                break

            peeked = self.peek()

        return "WHITESPACES", whitespaces

    def __tokenize_unquoted_value(self) -> Token:
        peeked = self.peek()

        unquoted_value_characters = ""
        while peeked is not None:
            if peeked in VALID_VALUE_CHARACTERS:
                unquoted_value_characters += self.consume()

            elif peeked == ESCAPE_CHARACTER:
                unquoted_value_characters += self.__escape()

            else:
                break

            peeked = self.peek()
        return "VALUE", unquoted_value_characters

    def __tokenize_double_quoted_value(self) -> Token:
        self.consume()  # escape the starting quotes

        peeked = self.peek()
        double_quoted_value_characters = ""

        while peeked is not None:
            if peeked == DOUBLE_QUOTES:
                self.consume()  # escape the ending quotes
                break

            if peeked in (
                VALID_VALUE_CHARACTERS
                + ASSIGNMENT_OPERATOR
                + SINGLE_QUOTE
                + WHITESPACES
            ):
                double_quoted_value_characters += self.consume()

            elif peeked == ESCAPE_CHARACTER:
                double_quoted_value_characters += self.__escape()

            else:
                err = f"unknown character '{peeked}'"

                raise TokenizerError(err)

            peeked = self.peek()

        return "VALUE", double_quoted_value_characters

    def __tokenize_single_quoted_value(self) -> Token:
        self.consume()  # escape the quotes

        peeked = self.peek()
        single_quoted_value_characters = ""

        while peeked is not None:
            if peeked == SINGLE_QUOTE:
                self.consume()  # escape the quotes
                break

            if peeked in (
                VALID_VALUE_CHARACTERS
                + ASSIGNMENT_OPERATOR
                + SINGLE_QUOTE
                + WHITESPACES
            ):
                single_quoted_value_characters += self.consume()

            elif peeked == ESCAPE_CHARACTER:
                single_quoted_value_characters += self.__escape()

            else:
                err = f"unknown character '{peeked}'"

                raise TokenizerError(err)

        return "VALUE", single_quoted_value_characters

    def __tokenize_assignment_operator(self) -> Token:
        value = self.consume()

        return "ASSIGN_OP", value

    def tokenize(self) -> list[Token]:
        """The tokenizer class for converting input string to tokens.

        Returns:
            list[str]: List of `Token`.
        """
        tokens: list[Token]
        tokens = []

        peeked = self.peek()
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
                err = f"unknown character '{peeked}'"

                raise TokenizerError(err)

            peeked = self.peek()

        return tokens


@dataclass
class Parser:
    """The Parser class for converting list of tokens into `Command`.

    Attributes:
        tokens (list[Token]): list of tokens.
    """

    tokens: list[Token]

    def __peek_token(self) -> Token | None:
        try:
            return self.tokens[0]
        except IndexError:
            return None

    def __consume_token(self) -> Token | None:
        return self.tokens.pop(0)

    def __escape_whitespace(self) -> None:
        peeked = self.__peek_token()

        if peeked is not None and peeked[0] == "WHITESPACES":
            self.__consume_token()

    def __check_unparsed(self) -> None:
        if len(self.tokens) != 0:
            err = f"unparsed tokens: {self.tokens}"

            raise ParserError(err)

    def __parse_arg(self) -> str:
        peeked = self.__peek_token()

        if peeked:
            if peeked[0] == "VALUE":
                token = self.__consume_token()

                if token:
                    return token[1]

                err = "expected value token, found None"
                raise ParserError(err)

            err = f"expected value token, found {peeked}"
            raise ParserError(err)

        err = "expected value token, found None"
        raise ParserError(err)

    def __parse_args(self) -> list[str]:
        return self.__recursive_parse_args([])

    def __recursive_parse_args(self, acc: list[str]) -> list[str]:
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

                    if peeked[0] == "ASSIGN_OP":
                        self.tokens = tokens
                        return acc

                    err = f"unknown token: {peeked}"
                    raise ParserError(err)

                return new_acc

            return acc

        return acc

    def __parse_assign_op(self) -> None:
        peeked = self.__peek_token()

        if peeked:
            if peeked[0] == "ASSIGN_OP":
                self.__consume_token()

                self.__escape_whitespace()

            else:
                err = f"expected a assign_operator token, found {peeked}"
                raise ParserError(err)
        else:
            err = "expected a assign_operator token, found None"
            raise ParserError(err)

    def __parse_kwarg(self) -> tuple[str, str]:
        peeked = self.__peek_token()

        if peeked and peeked[0] == "VALUE":
            kwarg_name = self.__parse_arg()

            self.__escape_whitespace()
            self.__parse_assign_op()
            self.__escape_whitespace()

            kwarg_value = self.__parse_arg()

            return kwarg_name, kwarg_value

        err = f"expected value token, found {peeked}"
        raise ParserError(err)

    def __parse_kwargs(self) -> list[tuple[str, str]]:
        return self.__recursive_parse_kwargs([])

    def __recursive_parse_kwargs(
        self,
        acc: list[tuple[str, str]],
    ) -> list[tuple[str, str]]:
        peeked = self.__peek_token()

        if peeked:
            if peeked[0] == "VALUE":
                acc = [*acc, self.__parse_kwarg()]

                self.__escape_whitespace()
                return self.__recursive_parse_kwargs(acc)

            err = f"expected value token, found {peeked}"
            raise ParserError(err)

        return acc

    def parse(self) -> Command:
        """Parses the tokens into `Command`.

        Returns:
            `Command`: The parsed command data.
        """
        self.__escape_whitespace()

        args = self.__parse_args()
        self.__escape_whitespace()

        kwargs = self.__parse_kwargs()
        self.__check_unparsed()

        return {"args": args, "kwargs": kwargs}


def parse(inp: str) -> Command:
    """Parses the dew command language into `Command`.

    Parameters:
        inp (str): The input to be parsed.

    Returns:
        Command: The parsed command data.
    """
    tokens = Tokenizer(inp).tokenize()

    return Parser(tokens).parse()
