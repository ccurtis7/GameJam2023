# This ML AI doesn't know the full state of the board, and that's it's current
# Weakness. But you have to simplify. Most progress would go into fully defining
# the state of the board for double pairs and garbage, to distinguish when to
# go or straight or not in these situations. Currently just manually assigns
# straight strategy as one option among many.
import numpy as np
from random import choice, randint, sample, random
from itertools import combinations as comb

def score(values, roll):
    """
    Automatically scores the roll. Outputs the money amount assigned to the roll.
    """
    counts = [0]*7
    for value in values:
        counts[value] += 1

    if 5 in counts:
        return '5K' + str(roll)
    elif 4 in counts:
        return '4K' + str(roll)
    elif (3 in counts) and (2 in counts):
        return 'FH' + str(roll)
    elif 3 in counts:
        return '3K' + str(roll)
    elif not (2 in counts) and (counts[1] == 0 or counts[6] == 0):
        return 'S' + str(roll)
    elif counts.count(2) == 2:
        return 'DP' + str(roll)
    else:
        return 'G' + str(roll)

def takingStock(values):
    counts = [0]*7
    locs = [0]*7
    for i, value in enumerate(values):
        counts[value] += 1
        if locs[value] == 0:
            locs[value] = [i]
        else:
            locs[value] = locs[value] + [i]
    return counts, locs

def straight(values):
    counts, locs = takingStock(values)
    keep = []
    for i in [2,3,4,5]:
        if i in values:
            keep.append(values.index(i))
    if (1 in values) & (6 in values):
        keep.append(values.index(1))
    elif 1 in values:
        keep.append(values.index(1))
    elif 6 in values:
        keep.append(values.index(6))
    reroll = [i for i in range(5) if i not in keep]
    return reroll

def whichReroll(selection, values):
    if selection == 'S':
        reroll = straight(values)
    else:
        values = values.copy()
        counts, locs = takingStock(values)
        ordered = []
        if selection == 0:
            return []
        elif selection < 0:
            down = [1, 6, 1]
        elif selection > 0:
            down = [5, 0, -1]

        for j in range(*down):
            idx = 0
            count = 0
            for i in range(counts.count(j)):
                if count == 0:
                    idx = counts.index(j)
                else:
                    idx = counts.index(j, idx+1)
                ordered = ordered + j*[idx]
                count += 1

        reroll = []
        for i in range(abs(selection)):
            idx = values.index(ordered[i])
            values[idx] = '.'
            reroll.append(idx)

    return reroll

def whichReroll2(selection, values):

    values = values.copy()
    counts, locs = takingStock(values)
    ordered = []
    if len(selection) == 0:
        return []
    else:
        down = [5, 0, -1]
        for j in range(*down):
            idx = 0
            count = 0
            for i in range(counts.count(j)):
                if count == 0:
                    idx = counts.index(j)
                else:
                    idx = counts.index(j, idx+1)
                ordered = ordered + j*[idx]
                count += 1

        reroll = []
        for i in selection:
            idx = values.index(ordered[i])
            values[idx] = '.'
            reroll.append(idx)

    return reroll

def garbageMakeID(values, roll):
    counts, locs = takingStock(values)
    state = counts.copy()
    state[0] = roll
    return ''.join([str(i) for i in state])

def whichReroll3(values, rerollSorted):
    # Create the sorted list from the state/ID
    vSorted = values.copy()
    vSorted.sort()
    vCleaned = values.copy()
    reroll = []
    for i in rerollSorted:
        # Find the locations to reroll in unsorted positions
        toFind = vSorted[i]
        re1 = vCleaned.index(toFind)
        vCleaned[re1] = '.'
        reroll.append(re1)

    return reroll

# Add in a random element?
def MLStrategy(values, roll, debug, memory, gameMemory):
    try:
        result = score(values, roll) # The result of the roll
        sel = choice(memory[result]) # Consults memory to select what to reroll
        # Keeps the size of the dictionary to a reasonable size.
        if len(list(memory[result])) > 1050:
            memory[result] = sample(list(memory[result]), 1000)

    except:
        # Reroll the 5 highest, 5 lowest, or straight strategy
        memory[result] = list(range(-5, 6))*3 + ['S']*3
        sel = choice(memory[result])

    # random element, to make sure training works out. Sometimes position is overwritten.
    # if random() < rand:
    #     pos = choice([i.start() + 1 for i in re.finditer('-', state)])
    if roll == 1:
        gameMemory = {result: sel}
    else:
        gameMemory[result] = sel

    return whichReroll(sel, values), memory, gameMemory


def MLStrategy2(values, roll, debug, memory, gameMemory):
    """
    A second self-learning bot that keeps track of the complete state of the
    dice, rather than a smaller portion of it.
    """
    counts, locs = takingStock(values)
    counts[0] = roll
    test = counts[1:]
    test.sort(reverse=True)
    id = ''.join([str(roll)] + [str(i) for i in test])
    try:
        sel = list(choice(memory[id]))
        if len(list(memory[id])) > 550:
            memory[id] = sample(list(memory[id]), 500)
    except:
        # possible rerolls
        test = []
        for i in range(6):
            test = test + list(comb(range(5), i))
        memory[id] = []
        for i in test:
            memory[id].append(list(i)*3)

        sel = choice(memory[id])

    if roll == 1:
        gameMemory = {id: sel}
    else:
        gameMemory[id] = sel

    return whichReroll2(sel, values), memory, gameMemory


def MLStrategy3(values, roll, debug, memory, gameMemory):
    """
    A modified bot strategy that keeps track of more states, but not all states.
    If there isn't a roll better than a 2, it saves the entire state of the roll
    in the form of the counts variable
    """
    counts, loc = takingStock(values)
    result = score(values, roll) # The result of the roll
    if np.max(counts) <= 2:
        result = garbageMakeID(values, roll)

    try:

        sel = choice(memory[result]) # Consults memory to select what to reroll
        # A loop for making sure the entry is a list or int, not a numpy array
        if (type(sel) == int) | (type(sel) == np.int32) | (type(sel) == np.int64):
            pass
        else:
            sel = list(sel)
        # Keeps the size of the dictionary to a reasonable size.
        if len(list(memory[result])) > 4050:
            memory[result] = sample(list(memory[result]), 4000)

    except:
        # Reroll the 5 highest, 5 lowest, or straight strategy
        memory[result] = list(range(-5, 6))*20
        # Combo strategy, add in all possible roll combinations.
        test = []
        for i in range(1,6):
            test = test + list(comb(range(5), i))*20
        for i in test:
            memory[result].append(list(i))

        sel = choice(memory[result])

    if random() < 0.00005:
        t = list(range(-5, 6))*3
        test = []
        for i in range(1,6):
            test = test + list(comb(range(5), i))*3
        for i in test:
            t.append(list(i))
        sel = choice(t)

    # random element, to make sure training works out. Sometimes position is overwritten.
    # if random() < rand:
    #     pos = choice([i.start() + 1 for i in re.finditer('-', state)])
    if roll == 1:
        gameMemory = {result: sel}
    else:
        gameMemory[result] = sel

    try:
        if (type(sel) == int) | (type(sel) == np.int32) | (type(sel) == np.int64):
            reroll = whichReroll(sel, values)
        else:
            reroll = whichReroll3(values, sel)
    except:
        print(sel, type(sel))
    return reroll, memory, gameMemory
