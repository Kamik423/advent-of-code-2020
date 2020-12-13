#!/usr/bin/env python3

import itertools
from typing import List

import aoc


def main() -> None:
    lines = aoc.get_lines(13)
    # lines = "939\n7,13,x,x,59,x,31,19".split("\n")
    timestamp = int(lines[0])
    buses = [int(bus) for bus in lines[1].split(",") if bus != "x"]
    earliest_departure = timestamp
    min_bus = min(buses, key=lambda bus: bus - (earliest_departure % bus))
    total_wait = min_bus - earliest_departure % min_bus
    result = min_bus * total_wait
    print(f"{earliest_departure=} {min_bus=} {total_wait=} {result=}")

    offsets = {
        bus: offset
        for offset, bus in enumerate(
            [int(bus) if bus != "x" else None for bus in lines[1].split(",")]
        )
        if bus is not None
    }

    print("\nPart 2")
    print(buses)
    jump = 1
    time = 0
    for bus in buses:
        print(f"Fixing bus {bus}")
        offset = offsets[bus]
        while (not (time + offset) % bus == 0) or time == 0:
            time += jump
        jump *= bus
    print(time)


if __name__ == "__main__":
    main()
