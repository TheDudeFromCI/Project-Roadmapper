#!/usr/bin/python

import os.path
import pygame
import pygame_textinput
import commands

TEXT_COLOR = (0, 0, 0)
INPUT_SIZE = 21
OUTPUT_SIZE = 18
X_OFFSET = 4
Y_OFFSET = 2
FONT = 'Ubuntu Mono'

"""
This class is a container for handling keyboard input to pass to the command handler
as well as rendering text to the screen. This class redirects command outputs to the
display.
"""
class Console():

    """
    Creates a new console object. This will also initalize an instance of a rendering
    surface and load a font to render with. This is created with the assumption pygame
    has already been initialized.

    Attributes:
        main -- A reference to the main application container.
        max_line -- The maximum number of output lines to keep. Defaults to 15.
        fadeout_time -- The number of seconds before a line fades out. Defaults to 30.
    """
    def __init__(self, main, max_lines = 15, fadeout_time = 30):
        self.main = main
        self.lines = []
        self.times = []
        self.surfaces = []
        self.fadeout_time = fadeout_time
        self.max_lines = max_lines

        # Console Input
        self.textinput = pygame_textinput.TextInput(font_family = FONT, font_size = INPUT_SIZE)

        # Console Font
        self.font = FONT
        if not os.path.isfile(self.font):
            self.font = pygame.font.match_font(self.font)
        self.font = pygame.font.Font(self.font, OUTPUT_SIZE)

    """
    Appends a new line to this console output.

    Attributes:
        line -- The line to print to the console.
    """
    def append(self, line):
        self.lines.insert(0, line)
        self.times.insert(0, self.main.visuals.time)
        self.surfaces.insert(0, self.font.render(line, 0, TEXT_COLOR))
        
        if len(self.lines) > self.max_lines:
            self.lines = self.lines[:self.max_lines - len(self.lines)]
            self.times = self.times[:self.max_lines - len(self.times)]
            self.surfaces = self.surfaces[:self.max_lines - len(self.surfaces)]

    """
    When called, handles keyboard events which come from pygame to
    update the console input, and command handling.

    Attributes:
        events -- A list of all events which occured since the
            previous frame.
    """
    def update(self, events):
        if self.textinput.update(events):
            command = self.textinput.get_text()
            if command != '':
                success, log = commands.parseCommand(self.main, command)
                self.textinput.clear_text()

                log.reverse()
                for line in log:
                    self.append(line)

    """
    Called to render the current console display to the given rendering
    surface.

    Attributes:
        bg -- The surface to render the console to.
    """
    def render(self, bg):
        bg.blit(self.textinput.get_surface(), (X_OFFSET, Y_OFFSET))

        time = self.main.visuals.time
        for index, line in enumerate(self.lines):
            lifespan = time - self.times[index]

            if lifespan >= self.fadeout_time + 1:
                continue
            if lifespan >= self.fadeout_time:
                self.surfaces[index].set_alpha((1 - (lifespan - self.fadeout_time)) * 255)
            
            bg.blit(self.surfaces[index], (X_OFFSET, Y_OFFSET + INPUT_SIZE + 1 + OUTPUT_SIZE * index))

    """
    Clears the console output.
    """
    def clear(self):
        self.lines = []
        self.times = []
        self.surfaces = []
