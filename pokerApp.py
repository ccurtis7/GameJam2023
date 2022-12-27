from random import randint
import sys
from graphics import *
from dieview import DieView
from button import Button
from interface import TextInterface, GraphicsInterface


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


class PokerApp:

    def __init__(self, interface):
        """
        Defines the starting state of the game. Creates the dice, sets money to
        100, and defines the chosen interface.
        """
        self.dice = Dice()
        self.money = 100
        self.interface = interface

    def run(self):
        """
        The main loop of the program. The player can keep playing as long as
        they have enough money for a round (10) and the player keeps rolling.
        """
        while self.money >= 10 and self.interface.wantToPlay():
            self.playRound()

        self.interface.close()

    def playRound(self):
        """
        Plays a single round of a game. A round consists of three die rolls.
        These rolls are handled by the dorolls method.
        """
        # Deduct money
        self.money = self.money - 10
        self.interface.setMoney(self.money)
        # Do the rolls and update dice
        self.doRolls()
        # Get score
        result, score = self.dice.score()
        self.interface.showResult(result, score)
        self.money = self.money + score
        self.interface.setMoney(self.money)

    def doRolls(self):
        """
        Manages the dice for a single round of a game. 
        """
        self.dice.rollAll()
        roll = 1
        self.interface.setDice(self.dice.values())
        toRoll = self.interface.chooseDice()

        while roll < 3 and toRoll != []:
            # roll the dice
            self.dice.roll(toRoll)
            # iterate the roll variable
            roll += 1
            # update the dice on the interface
            self.interface.setDice(self.dice.values())
            # select dice to roll again
            if roll < 3:
                toRoll = self.interface.chooseDice()


def main():
    """
    Runs the complete program, with the interface selected. The interface
    must be hard-coded in.
    """
    interface = GraphicsInterface()
    #interface.win.getMouse()
    app = PokerApp(interface)
    app.run()
    interface.close()

if __name__ == '__main__':
    main()
