#!/usr/bin/env python3

import aoc


def main() -> None:
    numbers = aoc.get_integers(1)
    for lower_index, lower in enumerate(numbers):
        for upper in numbers[lower_index:]:
            if lower + upper == 2020:
                print(lower * upper)
    for lower_index, lower in enumerate(numbers):
        for middle_index, middle in enumerate(numbers[lower_index:]):
            for upper in numbers[middle_index:]:
                if lower + middle + upper == 2020:
                    print(lower * middle * upper)


if __name__ == "__main__":
    main()
