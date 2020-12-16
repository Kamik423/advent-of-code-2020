#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import aoc
import more_itertools
import parse


@dataclass
class Field:
    title: str
    from1: int
    to1: int
    from2: int
    to2: int

    index: Optional[int] = None

    def matches(self, number: int) -> bool:
        return self.from1 <= number <= self.to1 or self.from2 <= number <= self.to2

    def matches_all(self, tickets: List[Ticket], index: int) -> bool:
        return all(self.matches(ticket.values[index]) for ticket in tickets)

    def __hash__(self):
        return hash(self.title)


@dataclass
class Ticket:
    values: List[int]

    def values_not_matching_any(self, fields: List[Field]) -> List[int]:
        return [
            value
            for value in self.values
            if not any(field.matches(value) for field in fields)
        ]


class Matrix:
    matrix: Dict[Field, Dict[int, bool]]
    tickets: List[Ticket]
    fields: List[Field]

    def __init__(self, tickets: List[Ticket], fields: List[Field]):
        self.tickets = tickets
        self.fields = fields

        self.matrix: Dict[Field, Dict[int, bool]] = {
            field: {
                index: field.matches_all(tickets, index)
                for index in range(len(tickets[0].values))
            }
            for field in fields
        }

    def print_matrix(self) -> None:
        columns = len(self.tickets[0].values)
        print(
            "                   "
            + "".join(str(i)[-1] for i in range(columns))
            + f"\n                  ┌{'─'*columns}┐"
        )
        for field in self.fields:
            print(f"{field.title:18}│", end="")
            for index in range(columns):
                if (matches := self.matrix.get(field)) is not None:
                    if (match := matches.get(index)) is not None:
                        print("█" if match else "░", end="")
                    else:
                        print(" ", end="")
                else:
                    if index == field.index:
                        print("×", end="")
                    else:
                        print(" ", end="")
            print("│")
        print(f"                  └{'─'*columns}┘")

    def solve(self, verbose: bool = False) -> None:
        strip_index: Optional[int] = None
        strip_field: Optional[Field] = None
        while 1:
            if strip_index is not None and strip_field is not None:
                strip_field.index = strip_index
                self.matrix = {
                    field: {
                        index: match
                        for index, match in matches.items()
                        if index != strip_index
                    }
                    for field, matches in self.matrix.items()
                    if field != strip_field
                }
                strip_index = None
            if verbose:
                self.print_matrix()
            for field, matches in self.matrix.items():
                if sum(matches.values()) == 1:
                    index = next(index for index, match in matches.items() if match)
                    strip_field = field
                    strip_index = index
                    if verbose:
                        print(f">>> Found field '{field.title}' is index {index}.")
                    break
            else:
                break


def main() -> None:
    blocks = aoc.get_str(16).strip().split("\n\n")

    fields: List[Field] = []
    tickets: List[Ticket] = []

    for line in blocks[0].split("\n"):
        field = Field(
            **parse.parse("{title}: {from1:d}-{to1:d} or {from2:d}-{to2:d}", line).named
        )
        fields.append(field)

    ticket_error_count = 0
    for line in [*blocks[1].split("\n")[1:], *blocks[2].split("\n")[1:]]:
        ticket = Ticket([int(word) for word in line.split(",")])
        if not (errors := ticket.values_not_matching_any(fields)):
            tickets.append(ticket)
        else:
            ticket_error_count += sum(errors)
    print(ticket_error_count)

    matrix = Matrix(tickets, fields)
    matrix.solve(verbose=True)

    factor = 1

    my_ticket = tickets[0]
    for field in fields:
        if "departure" in field.title and field.index is not None:
            factor *= my_ticket.values[field.index]
    print()
    print(f"Determined factor {factor}!")


if __name__ == "__main__":
    main()
