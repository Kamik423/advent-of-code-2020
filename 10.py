#!/usr/bin/env python3

import aoc
import more_itertools


def main() -> None:
    numbers = aoc.get_integers(10)
    numbers.sort()
    numbers = [0, *numbers, max(numbers) + 3]
    jumps = [0, 0, 0, 0]
    for a, b in more_itertools.pairwise(numbers):
        jumps[b - a] += 1
    print(jumps[1] * jumps[3])

    ways_to_reach = {0: 1}
    for number in numbers[1:]:
        way_count = 0
        keys = ways_to_reach.keys()
        for delta in [1, 2, 3]:
            if (target_number := number - delta) in keys:
                way_count += ways_to_reach[target_number]
        ways_to_reach[number] = way_count
    print(way_count)


if __name__ == "__main__":
    main()
