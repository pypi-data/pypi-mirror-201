import string
import random


def secret_key_generator(length: int = 70, exclude: list = None):
    available_characters = string.ascii_letters + string.digits + string.punctuation
    if exclude is not None:
        for char in exclude:
            available_characters = available_characters.replace(char, '')
    return ''.join(random.choices(available_characters, k=length))
