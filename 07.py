#!/usr/bin/env python3
from __future__ import annotations

from typing import Dict, List, Tuple

import aoc
from cached_property import cached_property


class Rule:
    # class variable
    all_rules: Dict[str, Rule] = {}

    child_rule_specs: List[Tuple[int, str]]

    @cached_property
    def child_rules(self) -> List[Tuple[int, Rule]]:
        return [
            (chile_rule_spec[0], Rule.all_rules[chile_rule_spec[1]])
            for chile_rule_spec in self.child_rule_specs
        ]

    @cached_property
    def contains_shiny_gold(self) -> bool:
        for _, child_rule in self.child_rules:
            if child_rule.color == "shiny gold" or child_rule.contains_shiny_gold:
                return True
        return False

    @cached_property
    def contained_bags(self) -> int:
        return sum(
            [factor + factor * rule.contained_bags for factor, rule in self.child_rules]
        )

    color: str

    def __init__(self, line: str):
        color, children = line.split(" contain ")
        self.color = color.rsplit(" ", 1)[0]
        self.child_rule_specs = []
        for child in children.split(", "):
            if "no other" in child:
                break
            specifier = child.rsplit(" ", 1)[0]
            amount, color = specifier.split(" ", 1)
            if amount in ["0", "no"]:
                break
            self.child_rule_specs.append((int(amount), color))
        Rule.all_rules[self.color] = self


def main() -> None:
    for line in aoc.getstr(7).strip().split("\n"):
        Rule(line)
    print(len([rule for rule in Rule.all_rules.values() if rule.contains_shiny_gold]))
    print(Rule.all_rules["shiny gold"].contained_bags)


if __name__ == "__main__":
    main()
