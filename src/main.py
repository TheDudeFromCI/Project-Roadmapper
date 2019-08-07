#!/usr/bin/python

from visuals import Visuals
from tasks import Timeline
from console import Console

"""
A simple wrapper for the main application instance.
"""
class Main():
    def __init__(self):
        self.timeline = Timeline()
        self.console = Console(self)
        self.visuals = Visuals(self)

"""
Start the application.
"""
if __name__ == '__main__':
    main = Main()
    main.visuals.loop()

