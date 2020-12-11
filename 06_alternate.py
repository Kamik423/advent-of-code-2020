#!/usr/bin/env python3

import string
from typing import Set

import aoc


def main() -> None:
    groups = aoc.get_str(6).strip().split("\n\n")
    print(sum([len({c for c in g if c != "\n"}) for g in groups]))
    print(sum(len(set.intersection(*[set(l) for l in g.split("\n")])) for g in groups))


if __name__ == "__main__":
    main()
