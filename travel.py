# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 22:40:51 2019

@author: Simon
"""

import random
import math
import matplotlib.pyplot as plt
from draw import Show

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
    cities = []
    
    def addCity(self, city):
        self.cities.append(city)
    
    def getCity(self,index):
        return self.cities[index]
    
    def numberOfCities(self):
        return len(self.cities)
    
class Tour:
    def __init__(self, citiesOrder, tour=None):
        self.citiesOrder = citiesOrder
        self.tour = []
        self.fitness = 0.0
        self.distance = 0
        if tour is not None:
            self.tour = tour
        else:
            for index in range(0, self.citiesOrder.numberOfCities()):
                self.tour.append(None)
       
            
    def generateIndividual(self):
        for index in range(0,self.citiesOrder.numberOfCities()):
            self.setCity(index,self.citiesOrder.getCity(index))
        random.shuffle(self.tour)
    
    def getCity(self, position):
        return self.tour[position]
    
    def setCity(self, position, city):
        self.tour[position] = city
        self.fitness = 0.0
        self.distance = 0
        
    def getFitness(self):
        if self.fitness == 0:
            self.fitness = 1/float(self.getDistance())
        return self.fitness
    
    def getDistance(self):
        if self.distance == 0:
            tourDistance = 0
            for index in range(0,self.tourSize()):
                fromCity = self.getCity(index)
                toCity = None
                if index+1 < self.tourSize():
                    toCity = self.getCity(index+1)
                else:
                    toCity = self.getCity(0)
                tourDistance += fromCity.distanceTo(toCity)
            self.distance = tourDistance
        return self.distance
    
    def tourSize(self):
        return len(self.tour)
    
    def containsCity(self, city):
        if(self.tour.count(city)>0):
            return True
        return False
    
class Population:
    def __init__(self, popSize, initial, citiesOrder):
        self.ToursList = []
        for index in range(0,popSize):
            self.ToursList.append(None)
        
        if initial:
            for i in range(0,popSize):
                makeTour = Tour(citiesOrder)
                makeTour.generateIndividual()
                self.saveTour(i,makeTour)
    
    def saveTour(self, index, tour):
        self.ToursList[index] = tour
        
    def getTour(self, index):
        return self.ToursList[index]
    
    def getFittest(self):
        fittest = self.ToursList[0]
        for index in range(1,self.popSize()):
            if fittest.getFitness() <= self.getTour(index).getFitness():
                fittest = self.getTour(index)
        return fittest
    
    def popSize(self):
        return len(self.ToursList)
    
class GA:
    def __init__(self, citiesOrder):
        self.citiesOrder = citiesOrder
        self.mutation = 0.15
        self.tournamentSize = 5
        self.elitism = True
    
    def evolvePop(self, pop):    
        newPop = Population(pop.popSize(), False, self.citiesOrder)
        
        elitismOffset = 0
        if self.elitism:
            newPop.saveTour(0, pop.getFittest())
            elitismOffset = 1
        
        for index in range(elitismOffset, newPop.popSize()):
            parent1 = self.tournamentSelect(pop)
            parent2 = self.tournamentSelect(pop)
            
            child = self.crossover(parent1,parent2)
            newPop.saveTour(index,child)
            
        for index in range(elitismOffset, newPop.popSize()):
            self.mutate(newPop.getTour(index))
            
        return newPop
    
    
    def crossover(self, parent1, parent2):
        child = Tour(self.citiesOrder)
        
        startPos = random.randint(0,parent1.tourSize()-1)
        endPos = random.randint(0,parent1.tourSize()-1)
        
        for index in range(0, child.tourSize()):
            if startPos < endPos and index > startPos and index < endPos:
                child.setCity(index, parent1.getCity(index))
            elif startPos > endPos:
                if not(index < startPos and index > endPos):
                    child.setCity(index, parent1.getCity(index))
        
        for index in range(0, parent2.tourSize()):
            if child.containsCity(parent2.getCity(index)) == False:
                for i in range(0, child.tourSize()):
                    if child.getCity(i) == None:
                        child.setCity(i, parent2.getCity(index))
                        break
        
        return child
    
    def mutate(self, tour):
        for index in range(0,tour.tourSize()):
            if random.random() < self.mutation:
                tourPos = random.randint(0,tour.tourSize()-1)
                
                city1 = tour.getCity(index)
                city2 = tour.getCity(tourPos)
                
                tour.setCity(tourPos, city1)
                tour.setCity(index, city2)
                
    def tournamentSelect(self, pop):
        tournament = Population(self.tournamentSize, False, self.citiesOrder)
        for index in range(0, self.tournamentSize):
            rand = random.randint(0,pop.popSize()-1)
            tournament.saveTour(index, pop.getTour(rand))   
        fittest = tournament.getFittest()
        return fittest


def showPath(generation):
    x = []
    y = []
    best = pop.getFittest()
    for i in range(0,best.tourSize()):
        city = best.getCity(i)
        x.append(city.getX())
        y.append(city.getY())
        
        
    city = best.getCity(0)
    x.append(city.getX())
    y.append(city.getY())
    distance = best.getDistance()
    Show.show(x, y, "Gen: " + str(generation) + "\nDist: " + f'{distance:.2f}')
    
    

cities = CityList()
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
cities.addCity(City(60, 80))
cities.addCity(City(120, 80))
cities.addCity(City(180, 60))
cities.addCity(City(20, 40))
cities.addCity(City(100, 40))
cities.addCity(City(200, 40))
cities.addCity(City(20, 20))
cities.addCity(City(60, 20))
cities.addCity(City(160, 20))
        
   

pop = Population(20,True, cities)
print("Initial distance: ",pop.getFittest().getDistance())

distanceList = []
ga = GA(cities)
distanceList.append(pop.getFittest().getDistance())
pop = ga.evolvePop(pop)
for i in range(0,100000):
    pop = ga.evolvePop(pop)
    distanceList.append(pop.getFittest().getDistance())
    if i % 1000 == 0:
        showPath(i)
    
print("Finished")
print("Final distance: ",pop.getFittest().getDistance())

plt.plot(distanceList)
plt.ylabel('Distance')
plt.xlabel('Generation')
plt.show()