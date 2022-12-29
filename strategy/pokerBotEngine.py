from random import randint
from interface import TextInterface, GraphicsInterface, AIInterface, BotInterface

class Dice:
    """
    A method for keeping track of the die rolls of the player. These die
    rolls have no visualization component built into it. That is handled by
    the Interface classes.
    """

    def __init__(self):
        """
        Initialize the values of the die
        """
        self.dice = [0]*5
        self.roll(range(5))

    def roll(self, which):
        """
        Roll the selected dice. Stored as random numbers between 1 and 6.
        """
        if type(which) == int:
            self.dice[which] = randint(1,6)
        else:
            for pos in which:
                self.dice[pos] = randint(1,6)

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

class GameState:
    def __init__(self, values, money, roll, hand):
        """
        Container for the game state to be passed along to functions
        """
        self.values = values
        self.money = money
        self.roll = roll
        self.hand = hand

class PokerAI:
    def __init__(self, interface, memory):
        """
        Defines the starting state of the game. Creates the dice, sets money to
        0, and defines the chosen interface.
        """
        self.dice = Dice()
        self.money = 0
        self.roll = 0
        self.interface = interface

        self.hand = 0
        self.memory = memory
        self.gameMemory = {}

    def gamestate(self):
        """
        Creates a GameState object to pass information to the functions
        """
        return GameState(self.dice.values(), self.money, self.roll, self.hand)

    def run(self):
        """
        The main loop of the program.
        """
        while self.interface.wantToPlay(self.gamestate()):
            self.hand += 1
            self.playRound()

        self.interface.close(self.gamestate())
        return self.memory

    def playRound(self):
        """
        Plays a single round of a game. A round consists of three die rolls.
        These rolls are handled by the doRolls method.
        """
        # Deduct money
        self.money = self.money - 10
        self.interface.displayStart(self.gamestate())
        # Do the rolls and update dice
        self.doRolls()
        # Get score
        result, score = self.dice.score()
        self.interface.showResult(self.gamestate(), result, score)
        self.money = self.money + score
        self.interface.displayEnd(self.gamestate())
        self.rewardAI(result)

    def doRolls(self):
        """
        Manages the dice for a single round of a game.
        """
        self.dice.roll(range(5))
        self.roll = 1
        self.interface.displayDice(self.gamestate())
        toRoll, self.memory, self.gameMemory = self.interface.chooseDice(self.gamestate(), self.memory, self.gameMemory)

        while self.roll < 3 and toRoll != []:
            # roll the dice
            self.dice.roll(toRoll)
            # iterate the roll variable
            self.roll += 1
            # update the dice on the interface
            self.interface.displayDice(self.gamestate())
            # select dice to roll again
            if self.roll < 3:
                toRoll, self.memory, self.gameMemory = self.interface.chooseDice(self.gamestate(), self.memory, self.gameMemory)

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

def PokerAppSelector():
    """
    Selector for the version of the PokerApp the user wants to play. The artificial intelligence
    requires a strategy function in the file strategy.py.
    """
    gamestyle = input('Player Poker Dice using [T]ext, [G]raphics, [A]rtificial Intelligence, or [L]earning Bot?')
    if gamestyle[0] in 'Tt':
        interface = TextInterface()
    elif gamestyle[0] in 'Gg':
        interface = GraphicsInterface()
    elif gamestyle[0] in 'Aa':
        interface = AIInterface()
    elif gamestyle[0] in 'Ll':
        interface = BotInterface()
    else:
        print('Invalid response.')
        return None
    return interface
