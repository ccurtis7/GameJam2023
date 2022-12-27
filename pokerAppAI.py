from random import randint
import sys
from dieview2a import DieView
from button2 import Button


class Dice:
    def __init__(self):
        self.dice = [0]*5
        self.rollAll()

    def roll(self, which):
        # which is a list of positions [1,3]
        for pos in which:
            self.dice[pos] = randint(1,6)

    def rollAll(self):
        self.roll(range(5))

    def score(self):
        # Return the name of the result and the dollar amount
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
        return self.dice[:]


class PokerApp:

    def __init__(self, interface):
        self.dice = Dice()
        self.money = 100
        self.interface = interface

    def run(self):

        while self.money >= 10 and self.interface.wantToPlay():
            self.playRound()

        self.interface.close()

    def playRound(self):
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


class TextInterface:

    def __init__(self):
        print('Welcome to dice poker')

    def setMoney(self, amt):
        print('You currently have ${}.'.format(amt))

    def setDice(self, values):
        print('Dice:', values)

    def wantToPlay(self):
        ans = input('Do you wish to try your luck? ')
        return ans[0] in 'yY'# returns a boolean

    def close(self):
        print('\nThanks for playing!')

    def showResult(self, result, score):
        #print('Dice:', values)
        print('{}. You win ${}.'.format(result, score))

    def chooseDice(self):
        return eval(input("Enter a list of which dice to change ([] to stop) "))


class GraphicsInterface:

    def __init__(self):
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
        center.move(-3*size, 0)
        self.dice = []
        for i in range(5):
            view = DieView(self.win, center, size)
            self.dice.append(view)
            center.move(1.5*size, 0)

    def addDiceButtons(self, center, width, height):
        center.move(-3*width, 0)
        for i in range(1, 6):
            label = 'Die {}'.format(i)
            b = Button(self.win, center, width, height, label)
            self.buttons.append(b)
            center.move(1.5*width, 0)

    def setMoney(self, amt):
        self.money.setText("${}".format(amt))

    def setDice(self, values):
        for i in range(5):
            self.dice[i].setValue(values[i])

    def wantToPlay(self):
        ans = self.choose(['Roll', 'Quit'])
        return ans == 'Roll'# returns a boolean

    def close(self):
        self.win.close()

    def showResult(self, result, score):
        #print('Dice:', values)
        if score > 0:
            self.msg.setText("{}! You win {}".format(result, score))
        else:
            self.msg.setText("You rolled {}".format(result))

    def choose(self, choices):
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

    def chooseDice(self):
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


class PokerAI:

    def __init__(self, interface):
        self.dice = Dice()
        self.money = 100
        self.interface = interface

    def run(self):

        while self.money >= 10 and self.interface.wantToPlay():
            self.playRound()

        self.interface.close(self.money)
        print('You lasted {} games'.format(self.interface.nthGame))

    def playRound(self):
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

    def doRolls(self):
        self.dice.rollAll()
        roll = 1
        self.interface.setDice(self.dice.values())
        toRoll = self.interface.chooseDice(self.dice.values())

        while roll < 3 and toRoll != []:
            # roll the dice
            self.dice.roll(toRoll)
            # iterate the roll variable
            roll += 1
            # update the dice on the interface
            self.interface.setDice(self.dice.values())
            # select dice to roll again
            if roll < 3:
                toRoll = self.interface.chooseDice(self.dice.values())


class TextAIInterface:

    def __init__(self):
        print('Welcome to dice poker')
        self.nthGame = 0

    def setMoney(self, amt):
        #print('You currently have ${}.'.format(amt))
        pass

    def setDice(self, values):
        #print('Dice:', values)
        pass

    def wantToPlay(self):
        if self.nthGame <= 50:
            ans = 'yes'
            self.nthGame += 1
        else:
            ans = 'no'
        return ans[0] in 'yY'# returns a boolean

    def close(self, amt):
        print('Game over. You have ${:.0f}.'.format(amt))

    def showResult(self, result, score):
        #print('Dice:', values)

        #print('{}. You win ${}.'.format(result, score))
        pass

    def chooseDice(self, values):
        counts = [0]*7
        locs = [0]*7
        for i, value in enumerate(values):
            counts[value] += 1
            if locs[value] == 0:
                locs[value] = [i]
            else:
                locs[value] = locs[value] + [i]

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


def main():
    winnings = []
    for i in range(500):
        interface = TextAIInterface()
        #interface.win.getMouse()
        app = PokerAI(interface)
        app.run()
        interface.close(app.money)
        winnings.append(app.money)

    sum = 0
    for i in winnings:
        sum += i
    print('Your average winnings are {:.2f}'.format(sum/500 - 100))

if __name__ == '__main__':
    main()
