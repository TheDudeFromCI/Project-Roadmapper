#!/usr/bin/python

import pygame

BACKGROUND_COLOR = (160, 160, 160)

"""
This class is a wrapper for all rendering and updating events which
occur for the application. This also handles windows and input event.
"""
class Visuals():

    """
    Creates a new visuals object. This will also initialize pygame and
    create a window in the process.

    Attributes:
        main -- A reference to the main application container.
        fps -- The framerate to render at. Defaults to 30.
        windowName -- The name of the window. Defaults to 'Project Roadmapper'.
    """
    def __init__(self, main, fps = 30, windowName = 'Project Roadmapper'):
        # Set class properties
        self.main = main
        self.fps = fps

        # Setup Pygame
        pygame.init()

        # Setup Window
        self.screen_size = (800, 600)
        self.update_surface()
        pygame.display.set_caption(windowName)

        # Setup framerate sync
        self.clock = pygame.time.Clock()
        self.time = 0

    """
    Called internally to update the surface and background size to match
    the window size.
    """
    def update_surface(self):
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        self.background = pygame.Surface(self.screen_size)

    """
    Starts the render loop. This will cause update events and rendering
    events to be called continuously until a close request is made. This
    function will also clean up whent the loop ends.
    """
    def loop(self):
        self.running = True
        while self.running:
            self.update()
            self.draw()
            
        self.quit()

    """
    Called internally to update timing and handle all pending events.
    """
    def update(self):
        # Update framerate
        self.time += self.clock.tick(self.fps) / 1000.0

        # Check for events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.VIDEORESIZE:
                self.screen_size = (event.w, event.h)
                self.update_surface()

        self.main.console.update(events)

    """
    Called internally to render the current image to the window.
    """
    def draw(self):
        bg = self.background
        
        # Clear screen
        bg.fill(BACKGROUND_COLOR)

        # Render console
        self.main.console.render(bg)

        # Update frame
        self.screen.blit(bg, (0, 0))
        pygame.display.update()

    """
    Called internally to clean up pygame and dispose resources.
    """
    def quit(self):
        pygame.quit()
