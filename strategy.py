def Strategy(values):
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
