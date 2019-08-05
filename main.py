#!/usr/bin/python

import commands
from tasks import Timeline

"""
A simple wrapper for the main application instance.
"""
class Main():
    def __init__(self):
        self.timeline = Timeline()

"""
Start the application.
"""
if __name__ == '__main__':
    main = Main()

    # Parse Raw Input
    while True:
        line = input('> ')

        if line == 'exit':
            break
        
        commands.parseCommand(main, line)
