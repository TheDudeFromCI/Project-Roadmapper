#!/usr/bin/python

import commands
import visuals
from tasks import Timeline
from console import Console

"""
A simple wrapper for the main application instance.
"""
class Main():
    def __init__(self):
        self.timeline = Timeline()
        self.console = Console()

"""
Start the application.
"""
if __name__ == '__main__':
    main = Main()
    main.visuals = visuals.Visuals(main)

    main.visuals.loop()
    # Parse Raw Input
    #while True:
        #line = input('> ')

        #if line == 'exit':
        #    break
        
        #commands.parseCommand(main, line)
