#!/usr/bin/env python3

import re
from functools import reduce
from typing import Dict, Iterable, List

import aoc
import more_itertools


def main() -> None:
    lines = aoc.get_lines(14)
    memory: Dict[int, int] = {}

    mask1s = 0b_0000_0000_0000_0000_0000_0000_0000_0000_0000
    mask0s = 0b_1111_1111_1111_1111_1111_1111_1111_1111_1111

    line_regex = re.compile(r"^([a-z]+)(?:\[(.+?)\])? = (.+)$")

    for line in lines:
        command, argument, value = line_regex.match(line).groups()
        if command == "mem":
            memory[int(argument)] = (int(value) & mask0s) | mask1s
        elif command == "mask":
            mask0s = 0
            mask1s = 0
            for character in value:
                mask0s <<= 1
                mask1s <<= 1
                if character == "X":
                    mask0s |= 1
                    mask1s |= 0
                elif character == "1":
                    mask0s |= 1
                    mask1s |= 1
                elif character == "0":
                    mask0s |= 0
                    mask1s |= 0
                else:
                    assert False, f"Invalid character {character} in mask"
        else:
            assert False, f"Invalid command {command}"
    print(sum(memory.values()))

    ############################################################################

    mask1s = 0b_0000_0000_0000_0000_0000_0000_0000_0000_0000
    mask0s = 0b_1111_1111_1111_1111_1111_1111_1111_1111_1111
    floats: List[int] = []
    memory = {}

    for line in lines:
        command, argument, value = line_regex.match(line).groups()
        if command == "mem":
            write_value = int(value)
            address = int(argument)
            newline = "\n"
            for floating_masks in more_itertools.powerset(floats):
                mask = reduce(lambda a, b: a | b, floating_masks, 0)
                local_address = ((int(argument) & mask0s) | mask1s) | mask
                memory[local_address] = write_value
        elif command == "mask":
            mask0s = 0
            mask1s = 0
            floats = []
            float_index = 0b_1_0000_0000_0000_0000_0000_0000_0000_0000_0000
            for character in value:
                mask0s <<= 1
                mask1s <<= 1
                float_index >>= 1
                if character == "X":
                    mask0s |= 0
                    mask1s |= 0
                    floats.append(float_index)
                elif character == "1":
                    mask0s |= 1
                    mask1s |= 1
                elif character == "0":
                    mask0s |= 1
                    mask1s |= 0
                else:
                    assert False, f"Invalid character {character} in mask"
        else:
            assert False, f"Invalid command {command}"
    print(sum(memory.values()))


if __name__ == "__main__":
    main()
