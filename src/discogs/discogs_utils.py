import random

import src.discogs.lib_discogs as lib_discogs


class SkipRelease(Exception):
    pass


class StopRelease(Exception):
    pass


class DiscogsSearchFailed(Exception):
    pass


def prompt(msg, klass=str):
    """Prompt the user for input."""
    char = random.choice(["-", "_", "~", ">", "*"])
    print(char * 4 + " " + msg)
    return klass(input().strip())


