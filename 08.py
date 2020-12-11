#!/usr/bin/env python3

from __future__ import annotations

from typing import List, Set

import aoc


class Instruction:
    opcode: str
    value: int
    cpu: CPU

    def __init__(self, line: str, cpu: CPU):
        self.opcode, value_string = line.split(" ")
        self.value = int(value_string)
        self.cpu = cpu

    def evaluate(self) -> None:
        if self.opcode == "jmp":
            self.cpu.instruction_pointer += self.value
            return

        self.cpu.instruction_pointer += 1
        if self.opcode == "nop":
            pass
        elif self.opcode == "acc":
            self.cpu.accumulator += self.value
        else:
            print(f"WARNING: OPCODE <{self.opcode}> now known!")

    def toggle(self) -> bool:
        if self.opcode == "nop":
            self.opcode = "jmp"
            return True
        if self.opcode == "jmp":
            self.opcode = "nop"
            return True
        return False


class CPU:
    instruction_pointer: int
    accumulator: int

    visited_instructions: Set[int]
    instructions: List[Instruction]

    def reset(self) -> None:
        self.instruction_pointer = 0
        self.accumulator = 0
        self.visited_instructions = set()

    def __init__(self, lines: List[str]):
        self.reset()
        self.instructions = [Instruction(line, self) for line in lines]

    def run(self) -> bool:
        while self.instruction_pointer < len(self.instructions):
            if self.instruction_pointer in self.visited_instructions:
                return False
            self.visited_instructions.add(self.instruction_pointer)
            self.instructions[self.instruction_pointer].evaluate()
        return True

    def try_fix(self, index: int) -> bool:
        if (instruction := self.instructions[index]).toggle():
            self.reset()
            if self.run():
                return True
            instruction.toggle()
        return False


def main() -> None:
    cpu = CPU(aoc.get_lines(8))
    cpu.run()
    print(f"Found with at accumulator at {cpu.accumulator}.")
    for index in range(len(cpu.instructions)):
        if cpu.try_fix(index):
            break
    print(f"FOUND: Instruction #{index}, accumulator is now {cpu.accumulator}.")


if __name__ == "__main__":
    main()
