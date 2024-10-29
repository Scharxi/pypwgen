import string
from random import choice
from typing import LiteralString

CHARS = string.ascii_letters
SPECIALS = string.punctuation
DIGITS = string.digits

import typer


def gen_password(length: int = 8, *, digits: LiteralString | None = DIGITS,
                 specials: LiteralString | None = SPECIALS) -> str:
    """
    Generates a secure password
    :param length: The length of the password
    :param digits: Set to None to disable digits
    :param specials: Set to None to disable special characters
    :return: the generated password
    """
    password: str = ""
    global CHARS
    if digits is not None:
        CHARS += digits

    if specials is not None:
        CHARS += specials

    for _ in range(length):
        password += choice(CHARS)
    return password


print(gen_password(16, specials=None))
