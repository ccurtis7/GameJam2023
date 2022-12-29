import pandas as pd

##### Boring Stuff

def list_to_string(dice):
    return 'R' + ''.join(str(die) for die in dice)

def get_list_of_dice():
    list_of_dice = [ [ [0, 0, 0, 0, 0, 0] ]  ]

    temp_rerolls = []
    for first in range(6):
        dice = [0] * 6
        dice[first] += 1
        if dice not in temp_rerolls:
            temp_rerolls.append(dice)
    list_of_dice.append(temp_rerolls)

    temp_rerolls = []
    for first in range(6):
        for second in range(6):
            dice = [0] * 6
            dice[first] += 1 
            dice[second] += 1 
            if dice not in temp_rerolls:
                temp_rerolls.append(dice)
    list_of_dice.append(temp_rerolls)

    temp_rerolls = []
    for first in range(6):
        for second in range(6):
            for third in range(6):
                dice = [0] * 6
                dice[first] += 1 
                dice[second] += 1 
                dice[third] += 1 
                if dice not in temp_rerolls:
                    temp_rerolls.append(dice)
    list_of_dice.append(temp_rerolls)

    temp_rerolls = []
    for first in range(6):
        for second in range(6):
            for third in range(6):
                for fourth in range(6):
                    dice = [0] * 6
                    dice[first] += 1 
                    dice[second] += 1 
                    dice[third] += 1 
                    dice[fourth] += 1 
                    if dice not in temp_rerolls:
                        temp_rerolls.append(dice)
    list_of_dice.append(temp_rerolls)

    temp_rerolls = []
    for first in range(6):
        for second in range(6):
            for third in range(6):
                for fourth in range(6):
                    for fifth in range(6):
                        dice = [0] * 6
                        dice[first] += 1 
                        dice[second] += 1 
                        dice[third] += 1 
                        dice[fourth] += 1 
                        dice[fifth] += 1 
                        if dice not in temp_rerolls:
                            temp_rerolls.append(dice)
    list_of_dice.append(temp_rerolls)
    
    return list_of_dice

def get_reroll_options(dice):
    rerolls = []
    for ones in range(dice[0] + 1):
        for twos in range(dice[1] + 1):
            for threes in range(dice[2] + 1):
                for fours in range(dice[3] + 1):
                    for fives in range(dice[4] + 1):
                        for sixes in range(dice[5] + 1):
                            rerolls.append([ones, twos, threes, fours, fives, sixes])
    return rerolls

################# Evaluators

def evaluate(counts):
    if 5 in counts:
        return 30
    elif 4 in counts:
        return 15
    elif (3 in counts) and (2 in counts):
        return 12
    elif 3 in counts:
        return 8
    elif not (2 in counts) and (counts[0] == 0 or counts[5] == 0):
        return 20
    elif counts.count(2) == 2:
        return 5
    else:
        return 0

def EV(list_of_rolls, EV_index):
    total_value = 0
    for roll in list_of_rolls:
        total_value += EV_index[list_to_string(roll)]
    return total_value / len(list_of_rolls)

############## Index Generation

def get_zero_roll_index(list_of_dice):
    all_rolls = list_of_dice[5]
    rolls = [ list_to_string(roll) for roll in all_rolls]

    EVs = []
    for roll in all_rolls:
        EVs.append(evaluate(roll))

    zero_roll_index = pd.DataFrame(list(zip(rolls, EVs)), columns = ['Roll', 'EV'])
    
    return zero_roll_index

def get_next_index(list_of_dice, previous_index):
    all_rolls = list_of_dice[5]
    rolls = [ list_to_string(roll) for roll in all_rolls]

    best_plays = []
    max_EVs = []

    for count, roll in enumerate(all_rolls):
        reroll_options = get_reroll_options(roll)
        
        holds = []
        EVs = []
        for reroll in reroll_options:
            hold = [ roll[i] - reroll[i] for i in range(6) ]
            reroll_count = sum(reroll)
            
            new_outcomes = []
            for new_dice in list_of_dice[reroll_count]:
                new_outcome = [ hold[i] + new_dice[i] for i in range(6) ]
                new_outcomes.append(new_outcome)
            
            holds.append(hold)
            EVs.append(EV(new_outcomes, previous_index))
        
        best_play = holds[EVs.index(max(EVs))]
        max_EV = EVs[EVs.index(max(EVs))]
        
        best_plays.append(best_play)
        max_EVs.append(max_EV)
        
    next_index = pd.DataFrame(list(zip(rolls, best_plays, max_EVs)), columns = ['Roll', 'Hold', 'EV'])
    
    return next_index
    
#########################

def get_indexes():
    list_of_dice = get_list_of_dice()
    
    zero_roll_index = get_zero_roll_index(list_of_dice)    
    zero_roll_index.sort_values('Roll').to_csv('Zero_rolls.csv', index = False)
    zero_roll_index = { roll: EV for (roll, EV) in zip(zero_roll_index['Roll'], zero_roll_index['EV'])}
    
    one_roll_index = get_next_index(list_of_dice, zero_roll_index)
    one_roll_index.sort_values('Roll').to_csv('One_roll.csv')
    one_roll_index = { roll: EV for (roll, EV) in zip(one_roll_index['Roll'], one_roll_index['EV'])}
    
    two_roll_index = get_next_index(list_of_dice, one_roll_index)
    two_roll_index.sort_values('Roll').to_csv('Two_rolls.csv')
    two_roll_index = { roll: EV for (roll, EV) in zip(two_roll_index['Roll'], two_roll_index['EV'])}

    three_roll_index = get_next_index(list_of_dice, two_roll_index)
    three_roll_index.sort_values('Roll').to_csv('Three_rolls.csv')
    three_roll_index = { roll: EV for (roll, EV) in zip(three_roll_index['Roll'], three_roll_index['EV'])}

    return 

get_indexes()