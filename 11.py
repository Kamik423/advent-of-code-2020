#!/usr/bin/env python3

from __future__ import annotations

import itertools
from enum import Enum
from typing import List, Tuple, Union

import aoc


class Seat(str, Enum):
    FLOOR = "."
    EMPTY = "L"
    OCCUPIED = "#"

    def emptied(self) -> Seat:
        if self == Seat.FLOOR:
            return Seat.FLOOR
        return Seat.EMPTY

    @property
    def unoccupied(self) -> bool:
        return self == Seat.FLOOR or self == Seat.EMPTY


class Board:
    width: int
    height: int
    board: List[List[Seat]]

    def __init__(self, grid: Union[Board, str]):
        if isinstance(grid, str):
            self.board = [[Seat(seat) for seat in line] for line in grid.split("\n")]
        else:  # isinstance(grid, Board)
            self.board = [[seat.emptied() for seat in line] for line in grid.board]

        self.height = len(self.board)
        self.width = len(self.board[0])

    def __repr__(self) -> str:
        return "\n".join("".join(seat.value for seat in line) for line in self.board)

    def __getitem__(self, key: Tuple[int, int]) -> Seat:
        x, y = key
        return self.board[y][x]

    def __setitem__(self, key: Tuple[int, int], value: Seat) -> None:
        x, y = key
        self.board[y][x] = value

    def neighbors(self, x: int, y: int) -> int:
        is_left = x == 0
        is_right = x + 1 == self.width
        is_top = y == 0
        is_bottom = y + 1 == self.height
        return (
            (0 if is_top or is_left else not self[x - 1, y - 1].unoccupied)
            + (0 if is_top else not self[x, y - 1].unoccupied)
            + (0 if is_top or is_right else not self[x + 1, y - 1].unoccupied)
            + (0 if is_right else not self[x + 1, y].unoccupied)
            + (0 if is_bottom or is_right else not self[x + 1, y + 1].unoccupied)
            + (0 if is_bottom else not self[x, y + 1].unoccupied)
            + (0 if is_bottom or is_left else not self[x - 1, y + 1].unoccupied)
            + (0 if is_left else not self[x - 1, y].unoccupied)
        )

    def visible_seat_in_direction(self, x: int, y: int, dx: int, dy: int) -> bool:
        while 1:
            x += dx
            y += dy
            if not (0 <= y < self.height and 0 <= x < self.width):
                break
            if self[x, y] == Seat.OCCUPIED:
                return True
            if self[x, y] == Seat.EMPTY:
                return False
        return False

    def visible_seats(self, x: int, y: int) -> int:
        return sum(
            [
                self.visible_seat_in_direction(x, y, dx, dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if not (dx == 0 and dy == 0)
            ]
        )

    def next(self) -> Board:
        new_board = Board(self)
        for x in range(self.width):
            for y in range(self.height):
                if self[x, y] != Seat.FLOOR:
                    neighbors = self.neighbors(x, y)
                    if neighbors == 0:
                        new_board[x, y] = Seat.OCCUPIED
                    elif neighbors >= 4:
                        new_board[x, y] = Seat.EMPTY
                    else:
                        new_board[x, y] = self[x, y]
        return new_board

    def next2(self) -> Board:
        new_board = Board(self)
        for x in range(self.width):
            for y in range(self.height):
                if self[x, y] != Seat.FLOOR:
                    neighbors = self.visible_seats(x, y)
                    if neighbors == 0:
                        new_board[x, y] = Seat.OCCUPIED
                    elif neighbors >= 5:
                        new_board[x, y] = Seat.EMPTY
                    else:
                        new_board[x, y] = self[x, y]
        return new_board

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Board):
            return all(
                a == b
                for line_a, line_b in zip(self.board, other.board)
                for a, b in zip(line_a, line_b)
            )
        else:
            return False

    @property
    def occupied_count(self) -> int:
        return sum(seat == Seat.OCCUPIED for line in self.board for seat in line)


def main() -> None:
    first_board = Board(aoc.get_str(11).strip())

    board = first_board
    for step in itertools.count(1):
        last_board = board
        board = last_board.next()
        if last_board == board:
            break
    print(
        f"After step {step} {board.occupied_count} seats were occupied. "
        "The previous state was identical."
    )

    board = first_board
    for step in itertools.count(1):
        last_board = board
        board = last_board.next2()
        if last_board == board:
            break
    print(
        f"After step {step} {board.occupied_count} seats were occupied. "
        "The previous state was identical."
    )


if __name__ == "__main__":
    main()
