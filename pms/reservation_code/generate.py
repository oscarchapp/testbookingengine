from random import choice, choices
from string import ascii_uppercase,digits
def get():

    return ''.join(choices(ascii_uppercase+digits,k=8))