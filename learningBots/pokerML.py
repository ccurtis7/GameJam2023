import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../strategy')
from random import randint
from strategy import Strategy, ProbStrategy
from studentStrategy import noRerollStrategy, rollTwiceStrategy
from probStrategy import ProbStrategy2
from MLStrategy import MLStrategy, MLStrategy2
import hdfdict
import h5py


class Dice:
    """
    A method for keeping track of the die rolls of the player. These die die
    rolls have no visualization component built into it. That is handled by
    the Interface classes.
    """

    def __init__(self):
        """
        Initialize the values of the die
        """
        self.dice = [0]*5
        self.rollAll()

    def roll(self, which):
        """
        Roll the selected dice. Stored as random numbers between 1 and 6.
        """
        for pos in which:
            self.dice[pos] = randint(1,6)

    def rollAll(self):
        """
        Roll all the dice.
        """
        self.roll(range(5))

    def score(self):
        """
        Automatically scores the roll. Outputs a string of the name of the roll,
        and the money amount assigned to the roll.
        """
        counts = [0]*7
        for value in self.dice:
            counts[value] += 1

        if 5 in counts:
            return "Five of a Kind", 30
        elif 4 in counts:
            return "Four of a Kind", 15
        elif (3 in counts) and (2 in counts):
            return "Full House", 12
        elif 3 in counts:
            return "Three of a Kind", 8
        elif not (2 in counts) and (counts[1] == 0 or counts[6] == 0):
            return 'Straight', 20
        elif counts.count(2) == 2:
            return "Two Pairs", 5
        else:
            return 'Garbage', 0

    def values(self):
        """
        Returns the current values of the dice.
        """
        return self.dice[:]


class PokerAI:
    """
    A modified version of the PokerApp designed to be run by the AI. This class
    should not require modification by the students, as the rolling strategy
    of the AI isn't managed here. Only minor changes are made, and the AI
    should be able to run with the PokerApp as well.
    """
    def __init__(self, interface, memory):
        """
        Defines the starting state of the game. Creates the dice, sets money to
        100, and defines the chosen interface.
        """
        self.dice = Dice()
        self.money = 100
        self.interface = interface

        self.memory = memory
        self.gameMemory = {}

    def run(self):
        """
        The main loop of the program. 50 games are hard-coded in through the
        TextAIInterface wantToPlay method.
        """
        while self.money >= 10 and self.interface.wantToPlay():
            self.playRound()

        self.interface.close(self.money)
        return self.memory
        #print('You lasted {} games'.format(self.interface.nthGame))

    def playRound(self):
        """
        Plays a single round of a game. A round consists of three die rolls.
        These rolls are handled by the dorolls method.
        """
        # Deduct money
        self.money = self.money - 10
        #self.interface.setMoney(self.money)
        # Do the rolls and update dice
        self.doRolls()
        # Get score
        result, score = self.dice.score()
        self.interface.showResult(result, score)
        self.money = self.money + score
        self.interface.setMoney(self.money)
        # Added in to modify memory
        self.rewardAI(result)

    def doRolls(self):
        """
        Manages the dice for a single round of a game.
        """
        self.dice.rollAll()
        roll = 1
        self.interface.setDice(self.dice.values())
        toRoll, self.memory, self.gameMemory = self.interface.chooseDice(self.dice.values(), roll, self.memory, self.gameMemory)

        while roll < 3 and toRoll != []:
            # roll the dice
            self.dice.roll(toRoll)
            # iterate the roll variable
            roll += 1
            # update the dice on the interface
            self.interface.setDice(self.dice.values())
            # select dice to roll again
            if roll < 3:
                toRoll, self.memory, self.gameMemory = self.interface.chooseDice(self.dice.values(), roll, self.memory, self.gameMemory)

    def rewardAI(self, result):
        if result == 'Five of a Kind':
            for state, selection in self.gameMemory.items():
                self.memory[state] = list(self.memory[state])
                self.memory[state] = self.memory[state] + [selection]*6
        elif result == 'Straight':
            for state, selection in self.gameMemory.items():
                self.memory[state] = list(self.memory[state])
                self.memory[state] = self.memory[state] + [selection]*4
        elif result == 'Four of a Kind':
            for state, selection in self.gameMemory.items():
                self.memory[state] = list(self.memory[state])
                self.memory[state] = self.memory[state] + [selection]*3
        elif result == 'Full House':
            for state, selection in self.gameMemory.items():
                self.memory[state] = list(self.memory[state])
                self.memory[state] = self.memory[state] + [selection]*2
        elif result == 'Three of a Kind':
            for state, selection in self.gameMemory.items():
                self.memory[state] = list(self.memory[state])
                self.memory[state] = self.memory[state] + [selection]*1
        elif result == 'Double Pair':
            pass
        else:
            for state, selection in self.gameMemory.items():
                for i in range(1):
                    try:
                        self.memory[state].remove(selection)
                    except:
                        pass



class TextAIInterface:
    """
    A modified version of the TextInterface designed for the PokerAI that
    reduces outputs to the terminal. Also hard-codes in a total of 50 rounds
    played.
    AI strategy is managed with the chooseDice method.
    """

    def __init__(self):
        """
        Initializes the interface.
        """
        #print('Welcome to dice poker')
        self.nthGame = 0

    def setMoney(self, amt):
        """
        Printing current money to the screen is deactivated.
        """
        #print('You currently have ${}.'.format(amt))
        pass

    def setDice(self, values):
        """
        Printing current dice values has been deactivated.
        """
        #print('Dice:', values)
        pass

    def wantToPlay(self):
        """
        Hard-codes in 50 games played. Automatically closes once 50 games
        are completed.
        """
        if self.nthGame <= 51:
            ans = 'yes'
            self.nthGame += 1
        else:
            ans = 'no'
        return ans[0] in 'yY'# returns a boolean

    def close(self, amt):
        """
        Prints closing message when game is over.
        """
        print('Game over. You have ${:.0f}.'.format(amt))

    def showResult(self, result, score):
        """
        Printing results to screen is deactivated.
        """
        #print('Dice:', values)
        #print('{}. You win ${}.'.format(result, score))
        pass

    def chooseDice(self, values, roll, memory, gameMemory):
        """
        Hard-codes in the rolling strategy of the AI. Currently contains an
        optimized rolling strategy that maximizes winnings.
        """
        return MLStrategy(values, roll, memory, gameMemory)


def main():
    winnings = []

    # load memory
    test1 = h5py.File('pokerAI.h5', 'r')
    memory = dict(hdfdict.load('pokerAI.h5'))
    test1.close()
    # Doing a memory cleaning
    #memory = {}

    for i in range(2000):
        interface = TextAIInterface()
        #interface.win.getMouse()
        app = PokerAI(interface, memory)
        memory = app.run()
        interface.close(app.money)
        winnings.append(app.money)

    # save memory
    test1 = h5py.File('pokerAI.h5', 'w')
    hdfdict.dump(memory, 'pokerAI.h5')
    test1.close()
    #print(memory)

    sum = 0
    for i in winnings:
        sum += i
    print('Your average winnings are {:.2f}'.format(sum/2000 - 100))

if __name__ == '__main__':
    main()
