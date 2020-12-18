#!/usr/bin/env python3
from __future__ import annotations

import string
from enum import Enum, auto
from functools import reduce
from typing import Iterable, Iterator, List, Optional, Union

import aoc


class Operation(str, Enum):
    ADDITION = "+"
    MULTIPLICATION = "*"

    def operation(self, left: int, right: int) -> int:
        if self == Operation.ADDITION:
            return left + right
        else:
            return left * right

    def apply_all(self, tokens: List[Union[int, Operation]]) -> None:
        while self in tokens:
            index = tokens.index(self)
            tokens.pop(index)
            left = tokens[index - 1]
            right = tokens.pop(index)
            assert isinstance(left, int) and isinstance(right, int)
            tokens[index - 1] = self.operation(left, right)

    @classmethod
    def from_token(cls, token: str) -> Optional[Operation]:
        try:
            return cls(token)
        except ValueError:
            return None


class Delimiter(str, Enum):
    BEGIN = "("
    END = ")"

    @classmethod
    def from_token(cls, token: str) -> Optional[Delimiter]:
        try:
            return cls(token)
        except ValueError:
            return None


def tokenize(line: str) -> Iterator[str]:
    stack = ""
    for item in line:
        if item == " ":
            if stack:
                yield stack
                stack = ""
        elif item in string.digits:
            stack += item
        elif item in "()":
            if stack:
                yield stack
                stack = ""
            yield item
        elif Operation.from_token(item) is not None:
            yield item
        else:
            assert False, f"Unknown character {item}"
    if stack:
        yield stack


def lex(tokens: Iterable[str]) -> Iterator[Union[Operation, Delimiter, int]]:
    for token in tokens:
        yield Operation.from_token(token) or Delimiter.from_token(token) or int(token)


def interprete(lexemes: Iterator[Union[Operation, Delimiter, int]]) -> int:
    accumulator = 0
    operation: Operation = Operation.ADDITION
    for lexeme in lexemes:
        if isinstance(lexeme, Operation):
            operation = lexeme
        elif lexeme == Delimiter.END:
            break
        else:
            value = interprete(lexemes) if isinstance(lexeme, Delimiter) else lexeme
            accumulator = operation.operation(accumulator, value)
    return accumulator


def interprete2(lexemes: Iterable[Union[Operation, Delimiter, int]]) -> int:
    lexeme_stack: List[Union[Operation, int]] = []
    for lexeme in lexemes:
        if isinstance(lexeme, Operation) or isinstance(lexeme, int):
            lexeme_stack.append(lexeme)
        elif lexeme == Delimiter.END:
            break
        else:  # lexeme == Delimiter.BEGIN:
            lexeme_stack.append(interprete2(lexemes))

    Operation.ADDITION.apply_all(lexeme_stack)
    Operation.MULTIPLICATION.apply_all(lexeme_stack)

    assert len(lexeme_stack) == 1 and isinstance(lexeme_stack[0], int)
    return lexeme_stack[0]


def main() -> None:
    print(sum(interprete(lex(tokenize(line))) for line in aoc.get_lines(18)))
    print(sum(interprete2(lex(tokenize(line))) for line in aoc.get_lines(18)))


if __name__ == "__main__":
    main()
