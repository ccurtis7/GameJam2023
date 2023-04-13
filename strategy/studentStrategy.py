import numpy as np
from random import randint

def noRerollStrategy(values, roll):
    return []

def rollTwiceStrategy(values, roll):
    if roll == 1:
        return [0, 1, 2, 3, 4]
    elif roll == 2:
        return []

def workingStrategy(values, roll):
    # Calculate how many of each number you have
    counts = [0]*7
    # Which dice are where?
    locs = [0]*7
    for i, value in enumerate(values):
        counts[value] += 1
        if locs[value] == 0:
            locs[value] = [i]
        else:
            locs[value] = locs[value] + [i]

    if 5 in counts:
        return []
    elif 4 in counts:
        return locs[counts.index(1)]
    else:
        return [0, 1, 2, 3, 4]
