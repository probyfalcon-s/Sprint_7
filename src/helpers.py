from string import ascii_lowercase
from random import choice
import pytest


@pytest.fixture(scope="function")
def generate_random_string():
    def _generate_random_string(length: int) -> str:
        return "".join(choice(ascii_lowercase) for _ in range(length))

    return _generate_random_string
