import numpy as np
from random import randint

def noRerollStrategy(values, roll):
    return []

def rollTwiceStrategy(values, roll):
    if roll == 1:
        return [0, 1, 2, 3, 4]
    elif roll == 2:
        return []
