import sys
from pathlib import Path

import requests

COOKIE_PATH = Path(sys.argv[0]).parent / "COOKIE.txt"
COOKIES = {"session": COOKIE_PATH.read_text()}
URL = "https://adventofcode.com/2020/day/{}/input"


def get(day: int):
    return requests.get(URL.format(day), cookies=COOKIES).content
