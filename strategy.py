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