#!/usr/bin/env python3

from math import cos, radians, sin
from typing import List

import aoc


class Ship:
    """
    ▲y      N          90
    │     W ● E    180 ● 0
    └──▶x   S         270
    """

    x: int
    y: int
    orientation: int

    waypoint_x: int
    waypoint_y: int

    commands: List[str]

    def __init__(self, commands: List[str]):
        self.x, self.y = (0, 0)
        self.waypoint_x, self.waypoint_y = (10, 1)
        self.orientation = 0
        self.commands = commands

    def run(self) -> None:
        for command in self.commands:
            action = command[0]
            value = int(command[1:])
            if action == "N":
                self.y += value
            elif action == "S":
                self.y -= value
            elif action == "E":
                self.x += value
            elif action == "W":
                self.x -= value
            elif action == "L":
                self.orientation += value
            elif action == "R":
                self.orientation -= value
            elif action == "F":
                self.x += int(cos(radians(self.orientation))) * value
                self.y += int(sin(radians(self.orientation))) * value
            else:
                assert False, f"Action '{action}' not known"

            while self.orientation >= 360:
                self.orientation -= 360
            while self.orientation < 0:
                self.orientation += 360

    def rotate_waypoint(self, angle: int) -> None:
        """Rotate waypoint counterclockwise for specified amount of degrees."""
        theta = radians(angle)
        self.waypoint_x, self.waypoint_y = (
            self.waypoint_x * int(cos(theta)) - self.waypoint_y * int(sin(theta)),
            self.waypoint_x * int(sin(theta)) + self.waypoint_y * int(cos(theta)),
        )

    def run2(self) -> None:
        for command in self.commands:
            action = command[0]
            value = int(command[1:])
            if action == "N":
                self.waypoint_y += value
            elif action == "S":
                self.waypoint_y -= value
            elif action == "E":
                self.waypoint_x += value
            elif action == "W":
                self.waypoint_x -= value
            elif action == "L":
                self.rotate_waypoint(value)
            elif action == "R":
                self.rotate_waypoint(-value)
            elif action == "F":
                for _ in range(value):
                    self.x += self.waypoint_x
                    self.y += self.waypoint_y
            else:
                assert False, f"Action '{action}' not known"

    @property
    def manhattan_distance(self) -> int:
        return abs(self.x) + abs(self.y)


def main() -> None:
    ship = Ship(aoc.get_lines(12))
    ship.run()
    print(ship.manhattan_distance)

    ship = Ship(aoc.get_lines(12))
    ship.run2()
    print(ship.manhattan_distance)


if __name__ == "__main__":
    main()
