#!/usr/bin/env python3

from typing import Dict

import aoc
from tqdm import tqdm

RELEVANTS = [2020, 30000000]


def main() -> None:
    starting_numbers = [int(word) for word in aoc.get_str(15).strip().split(",")]

    last_said: Dict[int, int] = {}
    delta: int
    for turn in tqdm(range(1, max(RELEVANTS))):
        number: int
        if turn <= len(starting_numbers):
            number = starting_numbers[turn - 1]
        else:
            number = delta
        delta = turn - last_said.get(number, turn)
        last_said[number] = turn
        if turn in RELEVANTS:
            tqdm.write(f"{turn} ==> {number}")


if __name__ == "__main__":
    main()
