# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 19:26:45 2019

@author: Simon
"""

import random


class Nim:
    def __init__(self, gameType=None, startPlayer=None):
        print("Setup Nim game")

        # Pick a game type
        if gameType is not None:
            self.type = gameType
        else:
            self.type = int(input("Play normal(1) or misere(2): "))

        # Pick a starting player
        if startPlayer is not None:
            self.currentPlayer = startPlayer
        else:
            self.currentPlayer = int(input("Start AI(1) or human(2): "))

        # Choose a random amount of piles 2 to 5
        self.numPiles = random.randint(2, 5)
        self.piles = []

        # Adding random amount of elements to piles between 1 and 15
        for _ in range(self.numPiles):
            self.piles.append(random.randint(1, 15))

        # Add elements if not at least 2n+1
        while sum(self.piles) < 2*self.numPiles + 1:
            pickPile = random.randint(0, self.numPiles-1)
            self.piles[pickPile] = self.piles[pickPile] + 1

        self.displayPiles()

    def displayPiles(self):
        for pile in self.piles:
            for _ in range(pile):
                print("|", end=" ")
            print("\n")

    def nextMove(self):
        self.piles.sort(reverse=True)
        print("Piles: " + str(self.piles) + " " + str(self.xor()))

        if self.currentPlayer == 1:
            print("Current player: AI")
            self.AIMove()
            self.currentPlayer = 2
        else:
            print("Current player: Human")
            self.HumanMove()
            self.currentPlayer = 1

        self.displayPiles()

    def AIMove(self):
        # AI moves according to optimal stategy
        xor = self.xor()
        # If game "balanced" AI is in a losing position, take only one element
        # hoping the human to make a wrong move
        if xor == 0:
            pileSize = 0
            pickPile = 0

            while pileSize == 0:
                pickPile = random.randint(0, self.numPiles-1)
                pileSize = self.piles[pickPile]

            self.piles[pickPile] = self.piles[pickPile] - 1
        else:
            # If game "unbalanced", AI is in a winning position
            maxValue = max(self.piles)
            maxIndex = self.piles.index(maxValue)
            # If misere stategy, change in endgame where only one pile has more
            # than 1 element
            if self.type == 2:
                numOfOnes = self.piles.count(1)

                if len(self.piles)-self.piles.count(0)-numOfOnes == 1:
                    if numOfOnes % 2 == 0:
                        self.piles[maxIndex] = 1
                    else:
                        self.piles[maxIndex] = 0
                    return 1

            # Find the value corresponding to the largest unbalanced bit
            xor = pow(2, len(bin(xor))-3)

            # Find largest pile contribution to the "unbalanced" state
            for x in self.piles:
                if xor & x != 0:
                    maxValue = x
                    break

            maxIndex = self.piles.index(maxValue)

            # Pick elements from piles until the game is "balanced"
            while xor != 0 and self.piles[maxIndex] > 0:
                self.piles[maxIndex] = self.piles[maxIndex] - 1
                xor = self.xor()

    def HumanMove(self):
        # Human pick pile and number of elements
        pickPile = -1
        pickNumber = -1

        # Check if picked pile is valid
        while pickPile == -1:
            try:
                pickPile = int(
                    input("Pick a pile(0," + str(len(self.piles)-1) + "): "))
            except:
                print("You entered an invalid pile number")
                pickPile = -1
                continue
            if pickPile < 0 or pickPile > len(self.piles) - 1:
                print("You entered an invalid pile number")
                pickPile = -1
            elif self.piles[pickPile] == 0:
                print("No elements in pile, pick another")
                pickPile = -1

        # Check if number of elements is valid
        while pickNumber > self.piles[pickPile] or pickNumber < 1:
            pickNumber = int(
                input("Pick number to take from pile(1," + str(self.piles[pickPile]) + "): "))

        self.piles[pickPile] -= pickNumber

    def StartGame(self):
        # require current player to move if all piles are not empty
        while max(self.piles) > 0:
            self.nextMove()
        print("Piles: " + str(self.piles))

        # Print winner
        if self.type == 1:
            if self.currentPlayer == 1:
                print("Human wins")
            else:
                print("Computer wins")
        else:
            if self.currentPlayer == 2:
                print("Human wins")
            else:
                print("Computer wins")

    # Find where there are "unbalanced" bits
    def xor(self):
        xor = 0
        for pile in self.piles:
            xor = xor ^ pile
        return xor


game = Nim(gameType=2, startPlayer=1)
game.StartGame()
