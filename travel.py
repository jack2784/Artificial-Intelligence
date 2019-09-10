# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 22:40:51 2019

@author: Simon
"""

import random
import math

class City:
    def __init__(self, x=None,y=None):
        self.x = random.randint(0,200)
        self.y = random.randint(0,200)
        if x is not None and y is not None:
            self.x = x
            self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def distanceTo(self,city):
        distanceX = abs(self.getX()-city.getX())
        distanceY = abs(self.getY()-city.getY())
        return math.sqrt(distanceX*distanceX+distanceY*distanceY)

class CityList:
    def __init__(self):
        self.cities = []
    
    def addCity(self, city):
        self.cities.append(city)
    
    def getCity(self,index):
        return self.cities[index]
    
    def numberOfCities(self):
        return len(self.cities)
    
class Tour:
    def __init__(self, tour=None):
        self.tour = []
        self.fitness = 0
        self.distance = 0
        if tour is not None:
            self.tour = tour
            
    def generateIndividual(self, cities):
        for index in range(0,cities.numberOfCities()):
            self.setCity(index,cities.getCity(index))
        random.shuffle(self.tour)
    
    def getCity(self, position):
        return self.tour[position]
    
    def setCity(self, position, city):
        print(self.tour)
        self.tour[position] = city
        self.fitness = 0
        self.distance = 0
        
    def getFitness(self):
        if self.fitness == 0:
            self.fitness = 1/self.getDistance()
        return self.fitness
    
    def getDistance(self):
        if self.distance == 0:
            tourDistance = 0
            for index in range(0,self.tourSize()):
                fromCity = self.getCity(index)
                if index+1 < self.tourSize():
                    toCity = self.getCity(index+1)
                else:
                    toCity = self.getCity(0)
                tourDistance += fromCity.distanceTo(toCity)
            self.distance = tourDistance
        return self.distance
    
    def tourSize(self):
        return len(self.tour)
    
    def cointainsCity(self, city):
        if(self.tour.count(city)>0):
            return True
        return False
    
class Population:
    def __init__(self, popSize, initial, cities):
        self.ToursList = []
        self.popSize = popSize
        if initial:
            for i in range(0,popSize):
                self.ToursList.append(Tour().generateIndividual(cities))
                
    
    def saveTour(self, index, tour):
        self.ToursList[index] = tour
        
    def getTour(self, index):
        return self.ToursList[index]
    
    def getFittest(self):
        fittest = self.ToursList[0]
        for index in range(1,self.popSize):
            print(self.getTour(index).getFitness())
            if fittest.getFitness() <= self.getTour(index).getFitness():
                fittest = self.getTour(index)
        return fittest
    
    def popSize(self):
        return len(self.ToursList)
    
class GA:
    mutation = 0.015
    tournamentSize = 5
    elitism = True
    
    def evolvePop(self, pop, cities):
        newPop = Population(pop.popSize, False, cities)
        
        elitismOffset = 0
        if self.elitism:
            newPop.saveTour(0, pop.getFittest())
            elitismOffset = 1
        
        for index in range(elitismOffset,newPop.popSize()):
            parent1 = self.tournamentSelect(pop)
            parent2 = self.tournamentSelect(pop)
            
            child = self.crossover(parent1,parent2)
            newPop.saveTour(index,child)
            
        for index in range(elitismOffset,newPop.popSize()):
            self.mutation(newPop.getTour(index))
            
        return newPop
    
    def crossover(self, parent1, parent2):
        child = self.Tour()
        
        startPos = random.randint(0,parent1.tourSize())
        endPos = random.randint(0,parent1.tourSize())
        
        for index in range(0, child.tourSize()):
            if startPos < endPos and index > startPos and index < endPos:
                child.setCity(index, parent1.getCity(index))
            elif startPos > endPos:
                if not(index < startPos and index > endPos):
                    child.setCity(index,parent1.getCity(index))
        
        for index in range(0, parent2.tourSize()):
            if child.cointainsCity(parent2.getCity(index)) == False:
                for i in range(0,child.tourSize()):
                    if not child.getCity(i):
                        child.setCity(i,parent2.getCity(i))
                        break
        return child
    
    def mutation(self, tour):
        for index in range(0,tour.tourSize()):
            if random.random() < self.mutation:
                tourPos = random.randint(0,tour.tourSize())
                
                city1 = tour.getCity(index)
                city2 = tour.getCity(tourPos)
                
                tour.setCity(tourPos, city1)
                tour.setCity(index, city2)
                
    def tournamentSelect(self, pop):
        tournament = Population(self.tournamentSize, False)
        for index in range(0, self.tournamentSize):
            rand = random.randint(0,pop.popSize())
            tournament.saveTour(index, pop.getTour(rand))
            
        fittest = tournament.getFittest()
        return fittest

cities =  CityList()
cities.addCity(City(60,200))
cities.addCity(City(180, 200))
cities.addCity(City(80, 180))
cities.addCity(City(140, 180))
cities.addCity(City(20, 160))
cities.addCity(City(100, 160))
cities.addCity(City(200, 160))
cities.addCity(City(140, 140))
cities.addCity(City(40, 120))
cities.addCity(City(100, 120))
cities.addCity(City(180, 100))               

pop = Population(50,True, cities)
print("Initial distance: ",pop.getFittest().getDistance())

pop = GA.evolvePop(pop, cities)
for i in range(0,100):
    pop = GA.evolvePop(pop, cities)
    
print("Finished")
print("Final distance: ",pop.getFittest().getDistance())
print(pop.getFittest())

#a = City()
#b = City()
#
#sds = CityList()
#sds.addCity(a)
#sds.addCity(b)
#print(sds.getCity(1).getX())
#print(b.getX())