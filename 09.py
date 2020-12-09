#!/usr/bin/env python3

from itertools import combinations
from typing import List, Set

import aoc
from more_itertools import pairwise


def main() -> None:
    numbers = [int(line) for line in aoc.getstr(9).strip().split("\n")]

    stack: List[int] = []
    for index, (appending_number, number) in enumerate(pairwise(numbers)):
        stack.append(appending_number)
        if len(stack) < 25:
            continue
        if len(stack) > 25:
            stack.pop(0)

        if any(a + b == number for a, b in combinations(stack, 2)):
            continue

        print(f"No combination found for {number} (#{index}).")

        target = number

        for length in range(2, len(numbers)):
            for start_index in range(len(numbers) - length + 1):
                segment = numbers[start_index : start_index + length]
                if sum(segment) == target:
                    print(
                        f"Found range {segment} "
                        f"at [{start_index} : {start_index + length}) "
                        f"length ({length})."
                    )
                    weakness = min(segment) + max(segment)
                    print(f"The weakness is {weakness}.")


if __name__ == "__main__":
    main()
