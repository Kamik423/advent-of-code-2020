#!/usr/bin/env python3
from __future__ import annotations

from typing import Dict, List, Tuple

import aoc
import regex
from cached_property import cached_property


class Graph:
    rules: Dict[str, Rule] = {}

    def __init__(self, description: str):
        for line in description.split("\n"):
            rule = Rule(line, self)
            self.rules[rule.color] = rule


class Rule:
    children_specs: Dict[str, int]

    @cached_property
    def children(self) -> List[Tuple[Rule, 1]]:
        return [
            (self.graph.rules[color], count)
            for color, count in self.children_specs.items()
        ]

    @cached_property
    def contains_shiny_gold(self) -> bool:
        return any(
            child.color == "shiny gold" or child.contains_shiny_gold
            for child, _ in self.children
        )

    @cached_property
    def contained_bags(self) -> int:
        return sum(
            [count * (child.contained_bags + 1) for child, count in self.children]
        )

    color: str
    graph: Graph

    def __init__(self, line: str, graph: Graph):
        self.graph = Graph
        match = regex.fullmatch(
            r"^([a-z ]+?) bags contain (?:(no|\d+) ([a-z ]+?) bags?(?:\.$|, ))+",
            line,
        )
        self.color = match[1]
        self.children_specs = {}
        for amount, color in zip(match.captures(2), match.captures(3)):
            if amount not in ["no", "0"]:
                self.children_specs[color] = int(amount)


def main() -> None:
    graph = Graph(aoc.get_str(7).strip())
    print(len([rule for rule in graph.rules.values() if rule.contains_shiny_gold]))
    print(graph.rules["shiny gold"].contained_bags)


if __name__ == "__main__":
    main()
