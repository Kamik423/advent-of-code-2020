#!/usr/bin/env python3

from typing import Dict

import aoc


def safe_int(value: str) -> int:
    try:
        return int(value)
    except:
        return -1


def validate_byr(data: Dict[str, str]) -> bool:
    return len(byr := data.get("byr", "")) == 4 and 1920 <= safe_int(byr) <= 2002


def validate_iyr(data: Dict[str, str]) -> bool:
    return len(iyr := data.get("iyr", "")) == 4 and 2010 <= safe_int(iyr) <= 2020


def validate_eyr(data: Dict[str, str]) -> bool:
    return len(eyr := data.get("eyr", "")) == 4 and 2020 <= safe_int(eyr) <= 2030


def validate_hgt(data: Dict[str, str]) -> bool:
    if len(hgt := data.get("hgt", "")) >= 4:
        unit = hgt[-2:]
        value = safe_int(hgt[:-2])
        return (
            unit == "cm" and 150 <= value <= 193 or unit == "in" and 59 <= value <= 76
        )
    return False


def validate_hcl(data: Dict[str, str]) -> bool:
    if len(hcl := data.get("hcl", "")) == 7 and hcl[0] == "#":
        for character in hcl[1:]:
            if character not in "0123456789abcdef":
                return False
        return True
    return False


def validate_ecl(data: Dict[str, str]) -> bool:
    return ((ecl := data.get("ecl", "")) != "") and ecl in [
        "amb",
        "blu",
        "brn",
        "gry",
        "grn",
        "hzl",
        "oth",
    ]


def validate_pid(data: Dict[str, str]) -> bool:
    return len(pid := data.get("pid", "")) == 9 and 0 <= safe_int(pid)


def validate_cid(data: Dict[str, str]) -> bool:
    return True


def main() -> None:
    passports = aoc.get_str(4).rstrip().split("\n\n")
    fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
    valid_passport_count = 0
    for passport in passports:
        remaining_fields = [
            field
            for field in fields
            if field
            not in [
                field.split(":")[0] for field in passport.replace("\n", " ").split(" ")
            ]
        ]
        if remaining_fields == [] or remaining_fields == ["cid"]:
            valid_passport_count += 1
    print(valid_passport_count)

    validated_passport_count = 0

    for passport in passports:
        data = {
            field.split(":")[0]: field.split(":")[1]
            for field in passport.replace("\n", " ").split(" ")
        }
        validated_passport_count += (
            validate_byr(data)
            and validate_iyr(data)
            and validate_eyr(data)
            and validate_hgt(data)
            and validate_hcl(data)
            and validate_ecl(data)
            and validate_pid(data)
            and validate_cid(data)
        )
    print(validated_passport_count)


if __name__ == "__main__":
    main()
