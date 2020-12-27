#!/usr/bin/env python3

from __future__ import annotations

import itertools
from enum import IntEnum
from typing import Any, Optional, Union

import aoc
import parse

TILE_SIZE = 10

SNAKE_KERNEL = [
    [True if character == "#" else False for character in line]
    for line in "                  # \n#    ##    ##    ###\n #  #  #  #  #  #   ".split(
        "\n"
    )
]


class Direction(IntEnum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3

    @property
    def opposite(self) -> Direction:
        return Direction(self + 2 if self + 2 < 4 else self - 2)

    @property
    def offset(self) -> Coordinate:
        if self == Direction.NORTH:
            return Coordinate(0, -1)
        elif self == Direction.WEST:
            return Coordinate(-1, 0)
        elif self == Direction.SOUTH:
            return Coordinate(0, 1)
        else:  # if self == Direction.EAST:
            return Coordinate(1, 0)


class Coordinate:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def offset_by(self, direction: Direction) -> Coordinate:
        return self + direction.offset

    def __add__(self, other: Union[Direction, Coordinate]) -> Coordinate:
        if isinstance(other, Direction):
            return self + other.offset
        else:
            return Coordinate(self.x + other.x, self.y + other.y)

    def __bool__(self) -> bool:
        return self.x != 0 or self.y != 0

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Coordinate) and other.x == self.x and other.y == self.y

    def __len__(self) -> int:
        return abs(self.x) + abs(self.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"C({self.x}, {self.y})"


class Tile:
    tile_id: int
    world: World
    array: list[list[Optional[bool]]]

    def __init__(self, world: World, data: str):
        self.tile_id = parse.search("Tile {:d}:", data)[0]
        self.array = [[pixel == "#" for pixel in line] for line in data.split("\n")[1:]]
        self.world = world

    def edge(self, direction: Direction) -> list[bool]:
        if direction == Direction.NORTH:
            return self.array[0]
        elif direction == Direction.SOUTH:
            return self.array[-1]
        elif direction == Direction.EAST:
            return [self.array[y][-1] for y in range(TILE_SIZE)]
        else:  # if direction == Direction.WEST:
            return [self.array[y][0] for y in range(TILE_SIZE)]

    def matches(self, tile: Tile, direction: Direction) -> bool:
        return self.edge(direction) == tile.edge(direction.opposite)

    def find_neighbor(
        self, unplaced_tiles: list[Tile], direction: Direction
    ) -> Optional[Tile]:
        target = self.world.coordinate(self).offset_by(direction)
        if target in self.world:
            return None
        for tile in unplaced_tiles:
            for _ in range(2):
                for _ in range(4):
                    if self.matches(tile, direction):
                        self.world[target] = tile
                        unplaced_tiles.remove(tile)
                        return tile
                    tile.rotate()
                tile.mirror()
        return None

    def dock(self, direction: Direction, target_direction: Direction) -> None:
        amount = target_direction - direction + 2
        while amount > 4:
            amount -= 4
        while amount < 0:
            amount += 4
        self.rotate(amount)

    def rotate(self, turns: int = 1) -> None:
        for _ in range(turns):
            max_x = len(self.array)
            max_y = len(self.array[0])
            self.array = [
                [self.array[x][max_y - y - 1] for x in range(max_x)]
                for y in range(max_y)
            ]

    def mirror(self) -> None:
        self.array = self.array[::-1]

    def matches_snake_at(self, x: int, y: int, overwrite: bool = False) -> bool:
        for y2, line in enumerate(SNAKE_KERNEL, y):
            for x2, must_be_true in enumerate(line, x):
                if y2 < len(self.array) and x2 < len(self.array[0]):
                    if must_be_true and self.array[y2][x2]:
                        if overwrite:
                            self.array[y2][x2] = None
                    elif must_be_true:
                        return False
                else:
                    return False
        if not overwrite:
            self.matches_snake_at(x, y, True)
        return True

    @property
    def count_snakes(self) -> int:
        for _ in range(2):
            for _ in range(4):
                snake_count = 0
                for y in range(len(self.array)):
                    for x in range(len(self.array[0])):
                        snake_count += self.matches_snake_at(x, y)
                if snake_count:
                    return snake_count
                self.rotate()
            self.mirror()
        return 0

    def pretty(self) -> str:
        return f"Tile {self.tile_id}:\n" + "\n".join(
            "".join("#" if pixel else "." for pixel in line) for line in self.array
        )

    def __repr__(self) -> str:
        return f"Tile {self.tile_id}"


class World(dict[Coordinate, Tile]):
    array: list[list[bool]]

    def coordinate(self, tile: Tile) -> Coordinate:
        return {v: k for k, v in self.items()}[tile]

    @property
    def simple_grid(self) -> str:
        min_x = min(coordinate.x for coordinate in self.keys())
        min_y = min(coordinate.y for coordinate in self.keys())
        max_x = max(coordinate.x for coordinate in self.keys())
        max_y = max(coordinate.y for coordinate in self.keys())

        acc = ""

        if len(self) > 0:
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    coord = Coordinate(x, y)
                    acc += str(self[coord]).split(" ")[1] if coord in self else "    "
                    acc += " "
                acc = acc[:-1]
                acc += "\n"
        return acc[:-1] if acc else ""

    @property
    def big_grid(self) -> str:
        min_x = min(coordinate.x for coordinate in self.keys())
        min_y = min(coordinate.y for coordinate in self.keys())
        max_x = max(coordinate.x for coordinate in self.keys())
        max_y = max(coordinate.y for coordinate in self.keys())

        acc = ""

        if len(self) > 0:
            for y in range(min_y, max_y + 1):
                for y2 in range(TILE_SIZE):
                    for x in range(min_x, max_x + 1):
                        coord = Coordinate(x, y)
                        acc += (
                            "".join(
                                "#" if pixel else "." for pixel in self[coord].array[y2]
                            )
                            if coord in self
                            else " " * TILE_SIZE
                        )
                        acc += " "
                    acc = acc[:-1]
                    acc += "\n"
                acc += "\n"
        return acc[:-1] if acc else ""

    @property
    def product(self) -> Optional[int]:
        min_x = min(coordinate.x for coordinate in self.keys())
        min_y = min(coordinate.y for coordinate in self.keys())
        max_x = max(coordinate.x for coordinate in self.keys())
        max_y = max(coordinate.y for coordinate in self.keys())

        tl = Coordinate(min_x, min_y)
        tr = Coordinate(max_x, min_y)
        bl = Coordinate(min_x, max_y)
        br = Coordinate(max_x, max_y)

        if tl in self and tr in self and bl in self and br in self:
            return (
                self[tl].tile_id
                * self[tr].tile_id
                * self[bl].tile_id
                * self[br].tile_id
            )
        return None

    def merge(self) -> Tile:
        array = []
        min_x = min(coordinate.x for coordinate in self.keys())
        min_y = min(coordinate.y for coordinate in self.keys())
        max_x = max(coordinate.x for coordinate in self.keys())
        max_y = max(coordinate.y for coordinate in self.keys())

        array = [
            [False for _ in range(((max_x - min_x + 1) * (TILE_SIZE - 2)))]
            for _ in range((max_y - min_y + 1) * (TILE_SIZE - 2))
        ]
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                for y2 in range(1, TILE_SIZE - 1):
                    for x2 in range(1, TILE_SIZE - 1):
                        array[(TILE_SIZE - 2) * (y - min_y) + y2 - 1][
                            (TILE_SIZE - 2) * (x - min_x) + x2 - 1
                        ] = self[Coordinate(x, y)].array[y2][x2]
        tile = Tile(self, "Tile 0:\n")
        tile.array = array
        return tile


def main() -> None:
    content = aoc.get_str(20).strip()
    # content = "Tile 2311:\n..##.#..#.\n##..#.....\n#...##..#.\n####.#...#\n##.##.###.\n##...#.###\n.#.#.#..##\n..#....#..\n###...#.#.\n..###..###\n\nTile 1951:\n#.##...##.\n#.####...#\n.....#..##\n#...######\n.##.#....#\n.###.#####\n###.##.##.\n.###....#.\n..#.#..#.#\n#...##.#..\n\nTile 1171:\n####...##.\n#..##.#..#\n##.#..#.#.\n.###.####.\n..###.####\n.##....##.\n.#...####.\n#.##.####.\n####..#...\n.....##...\n\nTile 1427:\n###.##.#..\n.#..#.##..\n.#.##.#..#\n#.#.#.##.#\n....#...##\n...##..##.\n...#.#####\n.#.####.#.\n..#..###.#\n..##.#..#.\n\nTile 1489:\n##.#.#....\n..##...#..\n.##..##...\n..#...#...\n#####...#.\n#..#.#.#.#\n...#.#.#..\n##.#...##.\n..##.##.##\n###.##.#..\n\nTile 2473:\n#....####.\n#..#.##...\n#.##..#...\n######.#.#\n.#...#.#.#\n.#########\n.###.#..#.\n########.#\n##...##.#.\n..###.#.#.\n\nTile 2971:\n..#.#....#\n#...###...\n#.#.###...\n##.##..#..\n.#####..##\n.#..####.#\n#..#.#..#.\n..####.###\n..#.#.###.\n...#.#.#.#\n\nTile 2729:\n...#.#.#.#\n####.#....\n..#.#.....\n....#..#.#\n.##..##.#.\n.#.####...\n####.#.#..\n##.####...\n##..#.##..\n#.##...##.\n\nTile 3079:\n#.#.#####.\n.#..######\n..#.......\n######....\n####.#..#.\n.#...#.##.\n#.#####.##\n..#.###...\n..#.......\n..#.###..."

    world = World()
    tiles = [Tile(world, tile) for tile in content.split("\n\n")]
    anchor = tiles.pop(0)
    coordinate = Coordinate(0, 0)
    world[coordinate] = anchor
    placed_tiles = [anchor]
    while placed_tiles:
        anchor = placed_tiles.pop()
        for direction in [
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST,
        ]:
            if (tile := anchor.find_neighbor(tiles, direction)) is not None:
                placed_tiles.append(tile)
    print(world.simple_grid)
    print(world.big_grid)
    print(world.product)

    picture = world.merge()
    print(picture.pretty())
    print(f"{picture.count_snakes} snakes")
    print(
        sum(
            sum([1 if ((pixel is not None) and pixel) else 0 for pixel in line])
            for line in picture.array
        )
    )


if __name__ == "__main__":
    main()
