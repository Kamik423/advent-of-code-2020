#!/usr/bin/env python3

from __future__ import annotations

import itertools
from abc import ABC
from typing import Any, Dict, Iterable, Optional, Set, Tuple, Union

import aoc

ADDITIONAL_DIMENSION_NAMES = "zwabcdefghijklmnopqrstuv"


class World(ABC):
    world: Dict[int, Dict[int, Set[int]]]  # default type hint for 3d
    # https://github.com/python/typing/issues/513
    # https://github.com/python/mypy/issues/3345

    dimensions: int
    enable: List[int]
    keep: List[int]

    def __init__(self, board: str = ""):
        self.world = {}
        for x, line in enumerate(board.split("\n")):
            for y, character in enumerate(line):
                if character == "#":
                    self[x, y] = True

    def __getitem__(self, coordinate: Iterable[int]) -> bool:
        x, y, *rest = coordinate
        if not rest:
            rest = [0] * (self.dimensions - 2)
        rest.reverse()
        layer = self.world
        for dimension in rest:
            layer = layer.get(dimension)
            if layer is None:
                break
        if layer is not None and (line := layer.get(y)) is not None:
            return x in line
        return False

    def __setitem__(self, coordinate: Iterable[int], value: bool) -> None:
        x, y, *rest = coordinate
        if not rest:
            rest = [0] * (self.dimensions - 2)
        rest.reverse()
        layer = self.world
        if value:
            for dimension in rest:
                if dimension not in layer:
                    layer[dimension] = {}
                layer = layer[dimension]
            if y not in layer:
                layer[y] = set()
            layer[y].add(x)
        else:
            for dimension in rest:
                layer = layer.get(dimension)
                if layer is None:
                    break
            if layer is not None and (line := layer.get(y)) is not None and x in line:
                line.remove(x)

    def flatsum(self, thing: Union[Dict[int, Any], Set[int]]) -> int:
        if isinstance(thing, Set):
            return len(thing)
        else:
            return sum(self.flatsum(item) for item in thing.values())

    @property
    def count(self) -> int:
        return self.flatsum(self.world)

    def min_value(self, dimension: int, target: Optional[Any] = None) -> int:
        if target == None:
            target = self.world
        if not target:
            return 0
        assert target is not None
        if dimension == self.dimensions - 1:
            if isinstance(target, Set):
                return min(target)
            else:
                assert isinstance(target, dict)
                return min(target.keys())
        else:
            assert isinstance(target, dict)
            return min(self.min_value(dimension + 1, item) for item in target.values())

    def max_value(self, dimension: int, target: Optional[Any] = None) -> int:
        if target == None:
            target = self.world
        assert target is not None
        if not target:
            return 0
        if dimension == self.dimensions - 1:
            if isinstance(target, Set):
                return max(target)
            else:
                assert isinstance(target, dict)
                return max(target.keys())
        else:
            assert isinstance(target, dict)
            return max(self.max_value(dimension + 1, item) for item in target.values())

    def dimension_name(self, dimension: int) -> str:
        return ["x", "y", *ADDITIONAL_DIMENSION_NAMES][dimension]

    def print_dimensions(self) -> None:
        for dimension in range(self.dimensions):
            print(
                f"{self.dimension_name(dimension)}: "
                f"[{self.min_value(dimension)} – {self.max_value(dimension)}]"
            )

    def __repr__(self) -> str:
        output = ""
        additional_dimensions: List[int] = []
        for dimension in range(self.dimensions - 2):
            additional_dimensions.append(
                list(
                    range(
                        self.min_value(dimension + 2), self.max_value(dimension + 2) + 1
                    )
                )
            )
        for dimension, addd in enumerate(itertools.product(*additional_dimensions)):
            output += (
                "\n"
                + ", ".join(
                    f"{self.dimension_name(dim + 2)}={addd[dim]}"
                    for dim in range(self.dimensions - 2)
                )
                + "\n"
            )
            for x in range(self.min_value(0), self.max_value(0) + 1):
                for y in range(self.min_value(1), self.max_value(1) + 1):
                    output += "#" if self[[x, y, *addd]] else "."
                output += "\n"
        return output[1:-1]

    def next(self) -> type(self):
        new_world = type(self)()
        for coordinate in itertools.product(
            *[
                list(
                    range(self.min_value(dimension) - 1, self.max_value(dimension) + 2)
                )
                for dimension in range(self.dimensions)
            ]
        ):
            new_world[coordinate] = self.next_at(coordinate)
        return new_world

    def next_at(self, coordinate: Iterable[int]) -> bool:
        neighbors = self.neighbors(coordinate)
        result = self.neighbors(coordinate) in (
            self.keep if self[coordinate] else self.enable
        )
        return self.neighbors(coordinate) in (
            self.keep if self[coordinate] else self.enable
        )

    def neighbors(self, coordinate: List[int]) -> int:
        return sum(
            (any(c != 0 for c in offset))
            and self[
                [
                    coordinate_ + offset_
                    for coordinate_, offset_ in zip(coordinate, offset)
                ]
            ]
            for offset in itertools.product([-1, 0, 1], repeat=self.dimensions)
        )


def main_verbose() -> None:
    string = aoc.get_str(17).strip()
    # string = ".#.\n..#\n###"
    world = World3D(string)
    print(world)
    for cycle in range(1, 7):
        world = world.next()
        print(f"\n==================== Cycle {cycle}\n")
        print(world)
    print(world.count)

    world = World4D(string)
    print(world)
    for cycle in range(1, 7):
        world = world.next()
        print(f"\n==================== Cycle {cycle}\n")
        print(world)
    print(world.count)


class World3D(World):
    keep = [2, 3]
    enable = [3]
    dimensions = 3


class World4D(World3D):
    dimensions = 4


def main() -> None:
    string = aoc.get_str(17).strip()
    world = World3D(string)
    for cycle in range(1, 7):
        world = world.next()
    print(world.count)

    world = World4D(string)
    for cycle in range(1, 7):
        world = world.next()
    print(world.count)


if __name__ == "__main__":
    main()
