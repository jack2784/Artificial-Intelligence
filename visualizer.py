# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 00:05:19 2019

@author: Simon

This code is just for visualization an is mostly copied from
http://blog.justsophie.com/python-knights-tour-revisited/
Adjustments have been made, to the looks and few funcionts
"""

import pygame
from pygame.locals import QUIT, KEYDOWN
import time
import random

class View(object):
    """ Provides a view of the chessboard with specified model """
    def __init__(self, model, size, speed):
        """ Initialize with the specified model """
        self.model = model
        self.screen = pygame.display.set_mode(size)
        self.speed = speed
        self.lines = []

    # Create chessboard
    def draw(self):
        """ Draw the game to the pygame window """
        self.screen.fill(pygame.Color('white'))

        for j in self.model.chessboard:
            for r in j:
                pygame.draw.rect(self.screen, pygame.Color('black'), r, 1)
        self.color_even()

        pygame.display.update()

    # Finding the global pixel position for the center of a square
    def center_pixel(self, r):
        c_pix = (r.x+(self.model.box_height/2), r.y+(self.model.box_height/2))
        return c_pix
    
    # Color visisted squares and drawing line between them
    def color_square(self, prev_square, square,k):
        i = square[1]
        j = square[0]

        r = self.model.chessboard[i][j]

        # Color current a special color
        pygame.draw.rect(self.screen, (255, 0, 0), r)
        # Color start a special color
        if prev_square == None:
            pygame.draw.rect(self.screen, (0, 255, 0), r)
        pygame.draw.rect(self.screen, pygame.Color('black'), r, 1)
        
        
        
        if prev_square != None:
            i_p = prev_square[1]
            j_p = prev_square[0]
            r_p = self.model.chessboard[i_p][j_p]
            
            # Color normal visited squares one color
            if k>1:
                pygame.draw.rect(self.screen, (255, 204, 255), r_p)
                pygame.draw.rect(self.screen, pygame.Color('black'), r_p, 1)
            
            # Find center of current and previous square
            c_pix_p = self.center_pixel(r_p)
            c_pix = self.center_pixel(r)
            
            # Draw line between them
            self.lines.append((c_pix_p, c_pix))
            for l in self.lines:
                pygame.draw.line(self.screen, pygame.Color('black'), l[0], l[1], 3)

        pygame.display.update()

    # Color ever other square a different color
    def color_even(self):
        NumSquares = self.model.w*self.model.h
        i = 0
        j = 0
        while i < self.model.w:
            while j < self.model.h:
                if (i+j)%2 == 0:
                    r = self.model.chessboard[i][j]
                    pygame.draw.rect(self.screen, (100, 204, 255), r)
                    pygame.draw.rect(self.screen, pygame.Color('black'), r, 1)
                j += 1
            j = 0
            i += 1

    # Animated path
    def animate_path(self):
        running = True
        quit_wait = True
        while running:
            self.draw()
            self.color_square(None, self.model.path[0],0)

            i = 1
            print("LENGTH PATH: ", len(self.model.path))
            while i < (len(self.model.path)) and running:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        quit_wait = False
                        pygame.display.quit()
                        pygame.quit()
                        running = False
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:                    
                        quit_wait = False
                        pygame.display.quit()
                        pygame.quit()
                        running = False
                        
                if running:
                    self.color_square(self.model.path[i-1], self.model.path[i],i)

                    if i == (len(self.model.path) - 2):
                        self.color_square(self.model.path[i], self.model.path[i+1],i)

                    i += 1
                    time.sleep(self.speed)
            running = False

        
        while quit_wait:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit_wait = False
                    pygame.display.quit()
                    pygame.quit()
                    #sys.exit(1)
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    quit_wait = False
                    pygame.display.quit()
                    pygame.quit()
                    running = False
                    #sys.exit(1)            

class Model(object):
    """ Represents the state of the chessboard"""
    def __init__(self, w, h, path, square_size):
        self.w = w
        self.h = h
        self.path = path

        self.box_height = square_size
        self.chessboard = []

        for i in range(self.w):
            row = []
            for j in range(self.h):
                r = pygame.Rect(i*self.box_height, j*self.box_height, self.box_height, self.box_height)
                row.append(r)
            self.chessboard.append(row)


if __name__ == '__main__':
    print("Visualizer, no function on its own")