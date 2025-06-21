import string
import secrets
from typing import List


def generate_random_password() -> str:
    """
    This function generate 8 digit random password
    """
    # ? Define character sets
    upper_case: str = string.ascii_uppercase
    lower_case: str = string.ascii_lowercase
    special_chars: str = string.punctuation
    digits: str = string.digits

    # ? Generate one character from each character set
    password: str = secrets.choice(upper_case)
    password += "".join(secrets.choice(lower_case) for _ in range(3))
    password += secrets.choice(special_chars)
    password += "".join(secrets.choice(digits) for _ in range(3))

    # ? Fill the rest of the password with random characters
    remaining_length: int = 8 - len(password)
    password += "".join(
        secrets.choice(string.ascii_letters + digits + special_chars)
        for _ in range(remaining_length)
    )

    # ? Shuffle the password to randomize the order
    password_list: List = list(password)
    secrets.SystemRandom().shuffle(password_list)
    password: str = "".join(password_list)
    return password
