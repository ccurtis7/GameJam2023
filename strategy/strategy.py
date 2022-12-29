import numpy as np
from random import randint

def Strategy(values, roll, debug):
    """
    The counts variable keeps track of the number of each kind of die.
    The locs variable keeps track of the locations of each kind of die.
    """
    counts = [0]*7
    locs = [0]*7
    for i, value in enumerate(values):
        counts[value] += 1
        if locs[value] == 0:
            locs[value] = [i]
        else:
            locs[value] = locs[value] + [i]

    # Strategy begins here.
    if 5 in counts:
        # IF you have five of a kind, don't reroll at all.
        return []
    elif 4 in counts:
        # If you have four of a kind, only reroll the one different value
        return [values.index(counts.index(1))]
    elif (3 in counts) and (2 in counts):
        # Don't reroll if you have a Full House
        return []
    elif 3 in counts:
        # IF a three, reroll the two odd ones out
        reroll = []
        for i, count in enumerate(counts):
            if count == 1:
                x = values.index(i)
                reroll.append(x)
        return reroll
    elif not (2 in counts) and (counts[1] == 0 or counts[6] == 0):
        # If straight, don't reroll
        return []
    # elif not (2 in counts) and (counts[1] == 1):
    #     # Four in a row
    #     return [0]
    # elif not (2 in counts) and (counts[6] == 1):
    #     # Four in a row
    #     return [5]
    # elif (counts[-2:] == [0,0]) | (counts[:3] == [0,0,0]) | ((counts[:2] == [0,0]) & (counts[-1] == 0)):
    #     # Four in a row
    #     return [values.index(counts.index(2))]
    elif counts.count(2) == 2:
        # If two pairs, only reroll one die
        return [values.index(counts.index(1))]
    elif counts.count(2) == 1:
        reroll = []
        for i, count in enumerate(counts):
            if count == 1:
                x = values.index(i)
                reroll.append(x)
        return reroll
    else:
        return [0,1,2,3,4]

    # reroll = []
    # return reroll

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

def probTwoRolls(N):
    p = 0
    for k in range(N+1):
        p += 6**(N-k)*(5**k)/(6**(2*N))
    return p

def probOneRoll(N):
    return 1/(6**N)

def prob(N, roll):
    if roll == 1:
        p = 0
        for k in range(N+1):
            p += 6**(N-k)*(5**k)/(6**(2*N))
        return p
    elif roll == 2:
        return 1/(6**N)

def score(values):
    """
    Automatically scores the roll. Outputs the money amount assigned to the roll.
    """
    counts = [0]*7
    for value in values:
        counts[value] += 1

    if 5 in counts:
        return 30
    elif 4 in counts:
        return 15
    elif (3 in counts) and (2 in counts):
        return 12
    elif 3 in counts:
        return 8
    elif not (2 in counts) and (counts[1] == 0 or counts[6] == 0):
        return 20
    elif counts.count(2) == 2:
        return 5
    else:
        return 0

scores = {'Five of a Kind': 30,
          'Four of a Kind': 15,
          'Three of a Kind': 8,
          'Full House': 12,
          'Straight': 20,
          'Two Pairs': 5}

def fiveOfAKind(values, roll):
    counts, locs = takingStock(values)
    keep = locs[np.argmax(counts)]
    reroll = [i for i in range(5) if i not in keep]

    # Calculate expected value
    ex = 2*score([values[i] for i in keep] + [randint(1,6) for i in range(5-len(keep))]) + prob(len(reroll), roll)*scores['Five of a Kind']
    return reroll, ex

def fourOfAKind(values, roll):
    counts, locs = takingStock(values)
    safe = np.max(counts)
    if safe >= 4:
        keep = [0, 1, 2, 3, 4]
        reroll = []
    else:
        keep = locs[np.argmax(counts)]
        reroll = [i for i in range(5) if i not in keep]
    ex = 1.5*score([values[i] for i in keep] + [randint(1,6) for i in range(5-len(keep))]) + prob(len(reroll), roll)*scores['Four of a Kind']
    return reroll, ex

def threeOfAKind(values, roll):
    counts, locs = takingStock(values)
    safe = np.max(counts)
    if safe >= 3:
        keep = [0, 1, 2, 3, 4]
        reroll = []
    else:
        keep = locs[np.argmax(counts)]
        reroll = [i for i in range(5) if i not in keep]
    ex = 1.5*score([values[i] for i in keep] + [randint(1,6) for i in range(5-len(keep))]) + prob(len(reroll), roll)*scores['Three of a Kind']
    return reroll, ex

def fullHouse(values, roll):
    counts, locs = takingStock(values)
    safe = np.max(counts)
    if (3 in counts) & (2 in counts):
        keep = [0, 1, 2, 3, 4]
        reroll = []
    elif safe == 5:
        reroll = locs[counts.index(5)][0:2]
        keep = [i for i in range(5) if i not in reroll]
    elif safe == 4:
        reroll = locs[counts.index(1)] + locs[counts.index(4)][0:1]
        keep = [i for i in range(5) if i not in reroll]
    elif safe <= 3:
        keep = locs[np.argmax(counts)]
        reroll = [i for i in range(5) if i not in keep]
    ex = 1.5*score([values[i] for i in keep] + [randint(1,6) for i in range(5-len(keep))]) + prob(len(reroll), roll)*scores['Full House']
    return reroll, ex

def straight(values, roll):
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
    ex = 1.5*score([values[i] for i in keep] + [randint(1,6) for i in range(5-len(keep))]) + prob(len(reroll), roll)*scores['Straight']
    return reroll, ex

def twoPairs(values, roll):
    counts, locs = takingStock(values)
    safe = np.max(counts)
    full, _ = fullHouse(values, 1)
    if (counts.count(2) == 2) | (full == []):
        reroll = []
        keep = [0, 1, 2, 3, 4]
    elif safe == 5:
        reroll = [0, 1]
        keep = [2, 3, 4]
    elif safe == 4:
        reroll = locs[counts.index(1)] + locs[counts.index(4)][0:2]
        keep = [i for i in range(5) if i not in reroll]
    elif safe == 3:
        keep = locs[counts.index(3)][0:2]
        reroll = [i for i in range(5) if i not in keep]
    elif safe == 2:
        keep = locs[counts.index(2)]
        reroll = [i for i in range(5) if i not in keep]
    else:
        reroll = [0,1,2,3,4]
        keep = []
    ex = 1.5*score([values[i] for i in keep] + [randint(1,6) for i in range(5-len(keep))]) + prob(len(reroll), roll)*scores['Two Pairs']
    return reroll, ex

def ProbStrategy(values, roll, debug):

    rerolls = {'Five of a Kind': fiveOfAKind,
           'Four of a Kind': fourOfAKind,
           'Three of a Kind': threeOfAKind,
           'Full House': fullHouse,
           'Straight': straight,
           'Two Pairs': twoPairs}

    expected = []
    toRolls = []
    for key, item in rerolls.items():
        reroll, ex = item(values, roll)
        expected.append(ex)
        toRolls.append(reroll)

    return toRolls[np.argmax(expected)]
