import re
from typing import Iterator, Callable

from hypersquirrel.literalinterpreter.instagram import interpret as interpret_instagram
from hypersquirrel.literalinterpreter.ehen import interpret as interpret_ehen

interpreters = {
    "^.*instagram.com\/(p|reel)\/[a-zA-z0-9-_]*.$": interpret_instagram,
    "^.*e-hentai\.org\/g\/[0-9]+\/.*$": interpret_ehen,
}


def get_interpreter(url: str) -> Callable[[str], Iterator[dict]]:
    for regex, interpreter in interpreters.items():
        if re.match(regex, url):
            return interpreter
