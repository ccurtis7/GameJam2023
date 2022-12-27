"""
a generic Button class for creating buttons on the GUI.
Buttons can be defined by the window in which they are created, the center
coordinate, the dimensions (width and height), and the label added to them.
Buttons have a single color, light gray. They can be activated or deactivated,
depending on whether the buttons are click-able or not.
"""
import sys
from graphics import *


class Button():

    def __init__(self, win, center, width, height, label):
        w, h = width/2.0, height/2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()


    def clicked(self, p):
        """
        Input a point p as input, returns a Boolean indicating whether the
        button has been clicked or not. The button must be active to be clicked.
        """
        return (self.active &
                (self.xmin <= p.getX() <= self.xmax) &
                (self.ymin <= p.getY() <= self.ymax))

    def getLabel(self):
        """
        Returns the label of the button
        """
        return self.label.getText()

    def activate(self):
        """
        Activates the state of the button by modifying the button width and
        label fill color.
        """
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = True

    def deactivate(self):
        """
        Deactivates the state of the button by modifying the button width and
        label fill color.
        """
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = False
