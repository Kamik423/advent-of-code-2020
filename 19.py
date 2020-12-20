#!/usr/bin/env python3

import re
import string
from typing import Dict, Union

import aoc


def rule_key_for_rule_index(index: Union[int, str]) -> str:
    return f"<<{index}>>"


def transpile(rule: str) -> str:
    return_stack = ""
    has_or = False
    for block in rule.split(" "):
        if len(block) >= 3 and block.startswith('"') and block.endswith('"'):
            return_stack += block[1:-1]
        elif block == "|":
            return_stack += "|"
            has_or = True
        elif len(block) > 0 and all(character in string.digits for character in block):
            return_stack += rule_key_for_rule_index(block)
        else:
            assert False, f"Unknown block '{block}' in rule"
    return f"({return_stack})" if has_or else return_stack


def main() -> None:
    content = aoc.get_str(19).strip()

    rule_strings, lines = content.split("\n\n")
    rules: Dict[int, str] = {
        int(rule_string.split(": ", 1)[0]): transpile(rule_string.split(": ", 1)[1])
        for rule_string in rule_strings.split("\n")
    }
    is_fulfilled = False
    while not is_fulfilled:
        is_fulfilled = True
        for rule_key, rule in rules.items():
            for key, replacement_rule in rules.items():
                rule = rule.replace(rule_key_for_rule_index(key), replacement_rule)
            rules[rule_key] = rule
            is_fulfilled = is_fulfilled and "<<" not in rule

    pattern = re.compile(f"^{rules[0]}$", re.MULTILINE)
    match_count = len(pattern.findall(lines))
    print(match_count)

    ###########################

    rule_strings, lines = content.split("\n\n")
    rules: Dict[int, str] = {
        int(rule_string.split(": ", 1)[0]): transpile(rule_string.split(": ", 1)[1])
        for rule_string in rule_strings.split("\n")
    }
    rules[8] = transpile("42 | 42 8")
    rules[11] = transpile("42 31 | 42 11 31")
    is_fulfilled = False
    max_depth = 4  # max(len(line) for line in lines.split("\n"))
    while not is_fulfilled and max_depth > 0:
        max_depth -= 1
        is_fulfilled = True
        for rule_key, rule in rules.items():
            for key, replacement_rule in rules.items():
                rule = rule.replace(rule_key_for_rule_index(key), replacement_rule)
            rules[rule_key] = rule
            is_fulfilled = is_fulfilled and "<<" not in rule

    pattern = re.compile(f"^{rules[0]}$", re.MULTILINE)
    match_count = len(pattern.findall(lines))
    print(match_count)


if __name__ == "__main__":
    main()
