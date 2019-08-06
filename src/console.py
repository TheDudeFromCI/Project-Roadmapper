#!/usr/bin/python

import pygame

class Console():
    def __init__(self):
        self.lines = []
        self.input = ''

    def type(self, key):
        self.input += key

    def backspace(self):
        if self.input != '':
            self.input = self.input[:-1]

