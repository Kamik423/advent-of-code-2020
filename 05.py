#!/usr/bin/env python3
from typing import List

import aoc


def main() -> None:
    seats = aoc.get_str(5).strip().split()
    seat_ids: List[int] = []
    for seat in seats:
        row = int(seat[:7].replace("F", "0").replace("B", "1"), 2)
        col = int(seat[7:].replace("L", "0").replace("R", "1"), 2)
        seat_id = 8 * row + col
        seat_ids.append(seat_id)
    max_seat_id = max(seat_ids)
    print(max_seat_id)
    for seat_id in range(int(0.1 * max_seat_id), int(0.9 * max_seat_id)):
        if (
            seat_id - 1 in seat_ids
            and seat_id not in seat_ids
            and seat_id + 1 in seat_ids
        ):
            print(seat_id)


if __name__ == "__main__":
    main()
