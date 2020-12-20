#!/usr/bin/env python3

from __future__ import annotations

import copy
import string
from typing import Dict, List, Optional, Tuple, Union

import aoc

Rules = Dict[int, "Rule"]


class MatchStack:
    data: str

    def __init__(self, data: str):
        self.data = data

    def matches(self, character: str) -> bool:
        if self.data.startswith(character):
            self.data = self.data[1:]
            return True
        return False

    @property
    def empty(self) -> bool:
        return not self.data

    def __repr__(self) -> str:
        return f"Match({self.data})"


class Rule:
    descriptor: str
    rules: Rules

    explanation: List[List[Union[str, int]]]

    def __init__(self, descriptor: str, rules: Rules):
        self.desriptor = descriptor
        self.rules = rules
        self.explanation = [
            [
                int(word)
                if all(character in string.digits for character in word)
                else word[1:-1]
                for word in component.split(" ")
            ]
            for component in self.desriptor.split(" | ")
        ]

    def matches_(self, match_stack: MatchStack, d: str = "") -> List[MatchStack]:
        matches: List[MatchStack] = []
        for rule in self.explanation:
            match: Optional[MatchStack] = MatchStack(match_stack.data)
            for subrule in rule:
                if match is None:
                    break
                if isinstance(subrule, str):
                    if not match.matches(subrule):
                        match = None
                else:
                    matchesx = self.rules[subrule].matches_(match, d + "    ")  # <----
                    # The issue lies here. Multiple possible matches are returned.
                    # When only the first match was returned it might have been the
                    # wrong correct match. thus multiple ones have to be returned.
                    # since the other architecture works now work on this one has
                    # been stopped.
            if match is not None:
                matches.append(match)
        return matches

    def matches(self, data: str) -> bool:
        match_stacks = self.matches_(MatchStack(data))
        return any(match_stack.empty for match_stack in match_stacks)

    def __repr__(self) -> str:
        return f"Rule({self.desriptor})"


def main() -> None:
    content = aoc.get_str(19).strip()

    # content = '0: 4 1 5\n1: 2 3 | 3 2\n2: 4 4 | 5 5\n3: 4 5 | 5 4\n4: "a"\n5: "b"\n\nababbb\nbababa\nabbbab\naaabbb\naaaabbb'
    content = """
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

aaaaabbaabaaaaababaa""".strip()

    """

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

    content = """
0: 1 0 1 | 1 1 | 2
1: 3 | 2 0
2: "b"
3: "a"

baaa
abaaaa


    """.strip()

    rule_strings, lines = content.split("\n\n")
    rules: Rules = {}
    rules.update(
        {
            int(rule_string.split(":", 1)[0]): Rule(
                rule_string.split(": ", 1)[1], rules
            )
            for rule_string in rule_strings.split("\n")
        }
    )

    for message in lines.split("\n"):
        print(message, rules[0].matches(message))

    return

    print(len([message for message in lines.split("\n") if rules[0].matches(message)]))

    rules[8] = Rule("42 | 42 8", rules)
    rules[11] = Rule("42 31 | 42 11 31", rules)
    print(len([message for message in lines.split("\n") if rules[0].matches(message)]))


if __name__ == "__main__":
    main()
