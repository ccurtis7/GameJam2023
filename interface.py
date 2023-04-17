"""
Built-in interfaces for the Poker app. Includes a TextInterface that can be
run from the terminal and a GraphicsInterface built using the graphics.py
package.

All interfaces must have displayMoney, displayDice, displayStart, displayEnd,
wantToPlay, close, showResult, and chooseDice methods. GS is a GameState object
that contains the dice values (values), the amount of money the player has
(money), the roll number for the current hand (roll), and the hand number (hand).

"""

from graphics import *
from dieview import DieView
from button import Button
from basicStrategy import RuleStrategy
from strategy.strategy import Strategy
from strategy.MLstrategy import MLStrategy, MLStrategy3

class TextInterface:
    """
    Text-based interface operated through the terminal.
    """
    def __init__(self):
        print('Welcome to dice poker')
        self.name = 'text'

    def displayStart(self, GS):
        self.displayMoney(GS)

    def displayEnd(self, GS):
        self.displayMoney(GS)

    def displayMoney(self, GS):
        print('You currently have ${}.'.format(GS.money))

    def displayDice(self, GS):
        print('Dice:', GS.values)

    def wantToPlay(self, GS):
        ans = input('Do you wish to try your luck? ')
        return ans[0] in 'yY'# returns a boolean

    def close(self, GS):
        print('\nThanks for playing!')

    def showResult(self, GS, result, score):
        """
        Displays the result of the roll and the money earned.
        """
        print('{}. You win ${}.'.format(result, score))

    def chooseDice(self, GS):
        """
        Prompts the user which dice they would like to roll. Must be
        zero-indexed (the first die is die 0).
        """
        return eval(input("Enter a list of which dice to change ([] to stop) "))


class GraphicsInterface:

    def __init__(self):
        """
        Sets the starting screen for the game. Includes a title, background,
        starting message, 5 dice (pre-set to value 1), buttons for clicking,
        the roll and quit buttons, and a money talley.
        """
        self.name = 'graphics'
        self.win = GraphWin("Dice Poker", 600, 400)
        self.win.setBackground('green3')
        banner = Text(Point(300, 30), "Welcome to the Poker Parlor")
        banner.setSize(24)
        banner.setStyle('bold')
        banner.draw(self.win)

        # Message to audience
        self.msg = Text(Point(300, 380), "Welcome to the dice table")
        self.msg.setSize(18)
        self.msg.draw(self.win)

        # Add each of the dice to the screen
        self.createDice(Point(300, 100), 75)

        # Create buttons for each dice
        self.buttons = []
        self.addDiceButtons(Point(300, 170), 75, 30)

        # Roll Dice, Score, Quit buttons

        b = Button(self.win, Point(300, 230), 80, 40, 'Roll')
        self.buttons.append(b)
        b = Button(self.win, Point(300, 280), 80, 40, 'Score')
        self.buttons.append(b)
        b = Button(self.win, Point(545, 370), 80, 40, 'Quit')
        self.buttons.append(b)

        # Money talley
        self.money = Text(Point(300, 325), "$100")
        self.money.setSize(18)
        self.money.draw(self.win)

    def createDice(self, center, size):
        """
        A helper method to draw the five dice to the screen.
        """

        center.move(-3*size, 0)
        self.dice = []
        for i in range(5):
            view = DieView(self.win, center, size)
            self.dice.append(view)
            center.move(1.5*size, 0)

    def addDiceButtons(self, center, width, height):
        """
        A helper method to draw the five dice buttons to the screen.
        """
        center.move(-3*width, 0)
        for i in range(1, 6):
            label = 'Die {}'.format(i)
            b = Button(self.win, center, width, height, label)
            self.buttons.append(b)
            center.move(1.5*width, 0)

    def displayStart(self, GS):
        self.displayMoney(GS)

    def displayEnd(self, GS):
        self.displayMoney(GS)

    def displayMoney(self, GS):
        """
        Updates the value of the money displayed on the screen.
        """
        self.money.setText("${}".format(GS.money))

    def displayDice(self, GS):
        """
        Updates the values of the dice shown on the screen.
        """
        for i in range(5):
            self.dice[i].setValue(GS.values[i])

    def wantToPlay(self, GS):
        """
        Returns True if the user wants to keep playing (indicated by hitting
        the Roll button). Exits if the user hits the Quit button.
        """
        ans = self.choose(['Roll', 'Quit'])
        return ans == 'Roll'# returns a boolean

    def close(self, GS):
        """
        Closes the window. Used to end the game.
        """
        self.win.close()

    def showResult(self, GS, result, score):
        #print('Dice:', values)
        if score > 0:
            self.msg.setText("{}! You win {}".format(result, score))
        else:
            self.msg.setText("You rolled {}".format(result))

    def choose(self, choices):
        """
        A generic method that creates a choice between two or more buttons for
        the user. The user must click one of the buttons available. Outputs
        the option selected by the user as a string, the label of the selected
        button.
        """

        buttons = self.buttons
        for b in buttons:
            if b.getLabel() in choices:
                b.activate()
            else:
                b.deactivate()

        while True:
            p = self.win.getMouse()
            for b in buttons:
                if b.clicked(p):
                    return b.getLabel()

        return # the label of the button that the user selected

    def chooseDice(self, GS):
        """
        Returns the dice the user selected for reroll.
        """
        choices = [] # no dice have been chosen yet

        while True:
            b = self.choose(['Die 1', 'Die 2', 'Die 3', 'Die 4', 'Die 5', 'Roll', 'Score'])

            if b[0] == 'D':
                i = int(b[4]) - 1
                if i in choices:
                    choices.remove(i)
                    self.dice[i].setColor('black')
                else:
                    choices.append(i)
                    self.dice[i].setColor('gray')
            else: # User clicked Roll or Score
                for d in self.dice:
                    d.setColor('black')
                if b == 'Score':
                    return []
                elif choices != []:
                    return choices

class AIInterface:
    """
    Text-based interface operated through the terminal.
    """
    def __init__(self):
        print('Welcome to AI Dice poker')
        self.name = 'ai'
        self.maxhands = int(input('How many hands? '))
        if type(self.maxhands) != int:
            self.maxhands = 100000

        debug = input('Use the debugger [Y/N]? ')
        if debug[0] in 'Yy':
            self.debug = True
        else:
            self.debug = False

    def displayStart(self, GS):
        if self.debug:
            print('Starting Hand {}. You currently have ${}.'.format(GS.hand, GS.money))

    def displayEnd(self, GS):
        if self.debug:
            print('Ending Hand {}. You currently have ${}.'.format(GS.hand, GS.money))

    def displayDice(self, GS):
        if self.debug:
            print('Dice:', GS.values)

    def wantToPlay(self, GS):
        if GS.hand == self.maxhands:
            return False
        return True

    def close(self, GS):
        print('Hands played: {}'.format(GS.hand))
        print('Net result: {}'.format(GS.money))
        print('Average result: {}'.format(GS.money/GS.hand))

    def showResult(self, GS, result, score):
        """
        Displays the result of the roll and the money earned.
        """
        if self.debug:
            print('{}. You win ${}.'.format(result, score))

    def chooseDice(self, GS):
        """
        Prompts the user which dice they would like to roll. Must be
        zero-indexed (the first die is die 0).
        """
        return RuleStrategy(GS.values, GS.roll, self.debug)

class BotInterface:
    """
    Text-based interface operated through the terminal.
    """
    def __init__(self):
        print('Welcome to AI Dice poker')
        self.name = 'bot'
        self.maxhands = int(input('How many hands? '))
        if type(self.maxhands) != int:
            self.maxhands = 100000

        debug = input('Use the debugger [Y/N]? ')
        if debug[0] in 'Yy':
            self.debug = True
        else:
            self.debug = False

    def displayStart(self, GS):
        if self.debug:
            print('Starting Hand {}. You currently have ${}.'.format(GS.hand, GS.money))

    def displayEnd(self, GS):
        if self.debug:
            print('Ending Hand {}. You currently have ${}.'.format(GS.hand, GS.money))

    def displayDice(self, GS):
        if self.debug:
            print('Dice:', GS.values)

    def wantToPlay(self, GS):
        if GS.hand == self.maxhands:
            return False
        return True

    def close(self, GS):
        print('Hands played: {}'.format(GS.hand))
        print('Net result: {}'.format(GS.money))
        print('Average result: {}'.format(GS.money/GS.hand))

    def showResult(self, GS, result, score):
        """
        Displays the result of the roll and the money earned.
        """
        if self.debug:
            print('{}. You win ${}.'.format(result, score))

    def chooseDice(self, GS, memory, gameMemory):
        """
        Prompts the user which dice they would like to roll. Must be
        zero-indexed (the first die is die 0).
        """
        return MLStrategy3(GS.values, GS.roll, self.debug, memory, gameMemory)
