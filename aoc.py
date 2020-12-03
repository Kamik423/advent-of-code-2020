import sys
from pathlib import Path

import requests

COOKIE_PATH = Path(sys.argv[0]).parent / "COOKIE.txt"
COOKIES = {"session": COOKIE_PATH.read_text()}
URL = "https://adventofcode.com/2020/day/{}/input"
CACHE_DIRECTORY = Path("input")
CACHE_FILE_NAME_TEMPLATE = "{:02d}.txt"


def cache_file_for_day(day: int) -> Path:
    return CACHE_DIRECTORY / CACHE_FILE_NAME_TEMPLATE.format(day)


def ensure_downloaded(day: int) -> None:
    cache_file = cache_file_for_day(day)
    if not cache_file.exists():
        CACHE_DIRECTORY.mkdir(exist_ok=True)
        cache_file.write_bytes(requests.get(URL.format(day), cookies=COOKIES).content)


def get(day: int) -> bytes:
    ensure_downloaded(day)
    return cache_file_for_day(day).read_bytes()


def getstr(day: int) -> str:
    ensure_downloaded(day)
    return cache_file_for_day(day).read_text()
