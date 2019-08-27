# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 19:26:45 2019

@author: Simon
"""

import random

class Nim:
    def __init__(self,gameType=None,startPlayer=None):
        # Create random amount of piles with random amount of elemenents 
        # Pick game type and starting player
        print("Setup Nim game")
        if gameType is not None:
            self.type = gameType
        else:
            self.type = int(input("Play normal(1) or misere(2): "))
        if startPlayer is not None:
            self.currentPlayer = startPlayer
        else:
            self.currentPlayer = int(input("Start AI(1) or human(2): "))
        self.numPiles = random.randint(2,5)
        self.piles = []
        #self.numPiles = 3
        #self.piles = [3,7,1]
        for x in range(self.numPiles):
            self.piles.append(random.randint(1,15))
        while sum(self.piles) < 2*self.numPiles + 1:
            pickPile = random.randint(0,self.numPiles-1)
            self.piles[pickPile] = self.piles[pickPile] + 1
    
        
    
    def nextMove(self):
        self.piles.sort(reverse=True)
        print("Piles: " + str(self.piles) + " " + str(self.xor()))
        if self.currentPlayer == 1:
            print("Current player: AI")
            self.AIMove()
            self.currentPlayer = 2
        else:
            print("Current player: Human")
            #self.AIMove()
            self.HumanMove()
            self.currentPlayer = 1
            
    def AIMove(self):
        # AI moves according to optimal stategi
        xor = self.xor()
        #print(xor)
        # If game "balance" AI is in a losing position take only one element
        # hoping the human to make a wrong move
        if xor == 0:
            pileSize = 0
            pickPile = 0
            while pileSize == 0:
                pickPile = random.randint(0,self.numPiles-1)
                pileSize = self.piles[pickPile]
            self.piles[pickPile] = self.piles[pickPile] - 1
        else:
            # If game "unbalanced" AI is in a winning position
            maxValue = max(self.piles)
            maxIndex = self.piles.index(maxValue)
            # IF misere stategi change in endgame where only one pile have more
            # than 1 element
            if self.type == 2:
                numOfOnes = self.piles.count(1)
                if len(self.piles)-self.piles.count(0)-numOfOnes == 1:
                    if numOfOnes % 2 == 0:
                        self.piles[maxIndex] = 1
                    else:
                        self.piles[maxIndex] = 0
                    return 1
            # Find largest pile contribution to the "unbalanced" state
            xor = pow(2,len(bin(xor))-3)
            for x in self.piles:
                if xor & x != 0:
                    maxValue = x
                    break
            maxIndex = self.piles.index(maxValue)
            # Pick elements from piles until the game is "balanced"
            while xor != 0 and self.piles[maxIndex]>0:
                self.piles[maxIndex] = self.piles[maxIndex] - 1
                xor = self.xor()
        #print(bin(xor))
        
    def HumanMove(self):
        # Human pick pile and number of elements
        pickPile = -1
        pickNumber = -1
        while pickPile > len(self.piles)-1 or pickPile < 0:
            pickPile = int(input("Pick a pile(0," +str(len(self.piles)-1) +"): "))
        while pickNumber > self.piles[pickPile] or pickNumber < 1:
            pickNumber = int(input("Pick number to take from pile(1," + str(self.piles[pickPile]) + "): "))
        self.piles[pickPile] -= pickNumber 
     
    def StartGame(self):
        # require current player to move if all piles are not empty
        while max(self.piles) > 0:
            self.nextMove()
        print("Piles: " + str(self.piles) + " " + str(self.xor()))
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
    
    def xor(self):
        xor = 0;
        for pile in self.piles:
            xor = xor^pile
        return xor
        
print("TEST")
game = Nim(2,1)
game.StartGame()
        