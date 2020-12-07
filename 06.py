#!/usr/bin/env python3

import string
from typing import Set

import aoc


def main() -> None:
    groups = aoc.getstr(6).strip().split("\n\n")

    accumulator = 0
    for group in groups:
        found_characters: Set[str] = set()
        for character in group:
            if character in string.ascii_lowercase:
                found_characters.add(character)
        accumulator += len(found_characters)
    print(accumulator)

    accumulator = 0
    for group in groups:
        lines = group.split("\n")
        all_characters = [
            character for character in lines[0] if character in string.ascii_lowercase
        ]
        for line in lines[1:]:
            for character in list(all_characters):
                if character not in line:
                    all_characters.remove(character)
        accumulator += len(all_characters)
    print(accumulator)


if __name__ == "__main__":
    main()
