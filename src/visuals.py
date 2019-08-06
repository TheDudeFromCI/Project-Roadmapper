#!/usr/bin/python

import os.path
import pygame
from pygame.locals import *
import pygame_textinput
import commands

class Visuals():
    def __init__(self, main, fps = 30, windowName = 'Project Roadmapper'):
        self.main = main
        pygame.init()
        
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.Surface(self.screen.get_size())

        pygame.display.set_caption(windowName)

        self.fps = fps
        self.clock = pygame.time.Clock()

        self.textinput = pygame_textinput.TextInput(font_family = 'Ubuntu Mono', font_size = 21)

        # Build console font
        self.font = 'Ubuntu Mono'
        if not os.path.isfile(self.font):
            self.font = pygame.font.match_font(self.font)
        self.font = pygame.font.Font(self.font, 18)
        self.console = []

    def loop(self):
        self.running = True
        while self.running:
            self.update()
            self.draw()
            
        self.quit()

    def update(self):
        # Update framerate
        self.clock.tick(self.fps)

        # Check for events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                
        # Push events to text editor
        if self.textinput.update(events):
            if self.textinput.get_text() != '':
                commands.parseCommand(self.main, self.textinput.get_text())
                self.console.insert(0, '> ' + self.textinput.get_text())

                if len(self.console) > 5:
                    self.console = self.console[:-1]
                
                self.textinput.clear_text()

    def draw(self):
        # Clear screen
        self.background.fill((160, 160, 160))

        # Render console text
        self.background.blit(self.textinput.get_surface(), (4, 0))

        for index, line in enumerate(self.console):
            self.background.blit(self.font.render(line, 0, (0, 0, 0)), (4, 22 + 18 * index))

        # Update frame
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()
        
    def quit(self):
        pygame.quit()
