import pandas as pd

def Strategy(values, roll, debug):
    """
    Requires the evaluation index CSV files
    """

    def list_to_string(dice):
        return 'R' + ''.join(str(die) for die in dice)

    def text_list_to_list(text_list):
        return [ int(text_list[1 + 3*i]) for i in range(6) ]

    if roll == 1:
        index = pd.read_csv('Two_rolls.csv')
    if roll == 2:
        index = pd.read_csv('One_roll.csv')

    counts = [0]*7
    locs = [[]]*7
    for i, value in enumerate(values):
        counts[value] += 1
        locs[value] = locs[value] + [i]

    counts = counts[1:]

    # Determine values to hold
    text_list = index[index['Roll'] == list_to_string(counts)]['Hold'].tolist()[0]

    hold = text_list_to_list(text_list)
    drop = [ counts[i] - hold[i] for i in range(6) ]

    drop_pos = locs[1][:drop[0]] + locs[2][:drop[1]] + locs[3][:drop[2]] + locs[4][:drop[3]] + locs[5][:drop[4]] + locs[6][:drop[5]]

    return drop_pos

def RuleStrategy(values, roll, debug):
    """
    Transferring Chad's strategy over for comparison.
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
