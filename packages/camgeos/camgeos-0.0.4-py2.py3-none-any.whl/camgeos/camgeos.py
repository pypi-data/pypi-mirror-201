"""Main module."""

import random
import string

def generate_random_string(length=10, upper=False, digits=False, punctuation=False):
    """Generates a random string with the given length including letters, upper case letters, digits and punctuation.

    Args:
        length (int, optional): The length of the string. Defaults to 10.
        upper (bool, optional): Whether to include upper case letters. Defaults to False.
        digits (bool, optional): Whether to include digits. Defaults to False.
        punctuation (bool, optional): Whether to include punctuation. Defaults to False.

    Returns:
        str: return a random string.
    """
    letters = string.ascii_lowercase
    if upper:
        letters += string.ascii_uppercase
    if digits:
        letters += string.digits
    if punctuation:
        letters += string.punctuation
    result_string = ''.join(random.choice(letters) for i in range(length))
    return result_string

def generate_lucky_number(length=10):
    """Generates a random lucky number with the given length.

    Args:
        length (int, optional): The length of the number. Defaults to 10.

    Returns:
        int: return a random number with the given length.
    """    
    lucky_number = random.randint(10**(length-1), 10**length-1)
    return lucky_number
    
