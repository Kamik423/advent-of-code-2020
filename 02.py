#!/usr/bin/env python3

import aoc


def main() -> None:
    count = 0
    for line in aoc.getstr(2).split("\n"):
        if line:
            password_format, password = line.split(": ")
            amounts, character = password_format.split(" ")
            minimal_count, maximal_count = [int(c) for c in amounts.split("-")]
            if minimal_count <= password.count(character) <= maximal_count:
                count += 1
    print(count)

    count = 0
    for line in aoc.getstr(2).split("\n"):
        if line:
            password_format, password = line.split(": ")
            positions, character = password_format.split(" ")
            first_position, last_position = [int(c) - 1 for c in positions.split("-")]
            if len(password) > last_position and (
                (password[first_position] == character)
                ^ (password[last_position] == character)
            ):
                count += 1
    print(count)


if __name__ == "__main__":
    main()
