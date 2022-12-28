import numpy as np


def Strategy(values, roll):
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

def fiveOfAKind(values):
    counts, locs = takingStock(values)
    keep = locs[np.argmax(counts)]
    reroll = [i for i in range(5) if i not in keep]
    return reroll

def fourOfAKind(values):
    counts, locs = takingStock(values)
    safe = np.max(counts)
    if safe >= 4:
        return []
    else:
        keep = locs[np.argmax(counts)]
        reroll = [i for i in range(5) if i not in keep]
        return reroll

def threeOfAKind(values):
    counts, locs = takingStock(values)
    safe = np.max(counts)
    if safe >= 3:
        return []
    else:
        keep = locs[np.argmax(counts)]
        reroll = [i for i in range(5) if i not in keep]
        return reroll

def fullHouse(values):
    counts, locs = takingStock(values)
    safe = np.max(counts)
    if (3 in counts) & (2 in counts):
        return []
    elif safe == 5:
        return locs[counts.index(5)][0:2]
    elif safe == 4:
        return locs[counts.index(1)] + locs[counts.index(4)][0:1]
    elif safe <= 3:
        keep = locs[np.argmax(counts)]
        return [i for i in range(5) if i not in keep]

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
    return [i for i in range(5) if i not in keep]


def twoPairs(values):
    counts, locs = takingStock(values)
    safe = np.max(counts)
    if (counts.count(2) == 2) | (fullHouse(values) == []):
        return []
    elif safe == 5:
        return [0, 1]
    elif safe == 4:
        return locs[counts.index(1)] + locs[counts.index(4)][0:2]
    elif safe == 3:
        keep = locs[counts.index(3)][0:2]
        return [i for i in range(5) if i not in keep]
    elif safe == 2:
        keep = locs[counts.index(2)]
        return [i for i in range(5) if i not in keep]
    else:
        return [0,1,2,3,4]

def ProbStrategy(values, roll):

    rerolls = {'Five of a Kind': fiveOfAKind(values),
               'Four of a Kind': fourOfAKind(values),
               'Three of a Kind': threeOfAKind(values),
               'Full House': fullHouse(values),
               'Straight': straight(values),
               'Two Pairs': twoPairs(values)}
    scores = {'Five of a Kind': 30,
              'Four of a Kind': 15,
              'Three of a Kind': 8,
              'Full House': 12,
              'Straight': 20,
              'Two Pairs': 5}

    expected = []
    toRolls = []
    for key, item in rerolls.items():
        if key == 'Straight':
            correction = 0.0001
        else:
            correction = 1
        if roll == 1:
            expected.append(correction*probTwoRolls(len(item))*scores[key])
        elif roll == 2:
            expected.append(correction*probOneRoll(len(item))*scores[key])
        toRolls.append(item)

    return toRolls[np.argmax(expected)]
