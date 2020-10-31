from secrets import choice
from string import ascii_lowercase


def generate_slug(length: int = 30) -> str:
    letters = [None for _ in range(length)]
    for i in range(length):
        letters[i] = choice(ascii_lowercase)
    return ''.join(letters)
