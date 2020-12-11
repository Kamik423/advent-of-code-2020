#!/usr/bin/env python3

import aoc


def main() -> None:
    board = [line for line in aoc.get_lines(3) if line]

    def is_tree(x: int, y: int) -> bool:
        return board[y][x % len(board[0])] == "#"

    def count_trees(dx: int, dy: int) -> int:
        x = 0
        y = 0
        tree_count = 0
        while 1:
            x += dx
            y += dy
            if y >= len(board):
                break
            tree_count += is_tree(x, y)
        return tree_count

    accumulator = 1
    for dx, dy in [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]:
        result = count_trees(dx, dy)
        print(f"- Right {dx}, down {dy}: {result}")
        accumulator *= result

    print(f"==> {accumulator}")


if __name__ == "__main__":
    main()
