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
    def __init__(self, x=None, y=None):
        if x is None or y is None:
            self.x = random.randint(0, 200)
            self.y = random.randint(0, 200)
        else:
            self.x = x
            self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distanceTo(self, city):
        distanceX = abs(self.getX() - city.getX())
        distanceY = abs(self.getY() - city.getY())
        return math.sqrt(distanceX**2 + distanceY**2)


class CityList:
    cities = []

    def addCity(self, city):
        self.cities.append(city)

    def getCity(self, index):
        return self.cities[index]

    def numberOfCities(self):
        return len(self.cities)


class Tour:
    def __init__(self, citiesOrder, tour=None):
        self.citiesOrder = citiesOrder
        self.tour = []
        self.fitness = 0
        self.distance = 0

        if tour is not None:
            self.tour = tour
        else:
            self.tour = [None] * self.citiesOrder.numberOfCities()

    def generateIndividual(self):
        for index in range(0, self.citiesOrder.numberOfCities()):
            self.setCity(index, self.citiesOrder.getCity(index))
        random.shuffle(self.tour)

    def getCity(self, position):
        return self.tour[position]

    def setCity(self, position, city):
        self.tour[position] = city
        self.fitness = 0
        self.distance = 0

    def getFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.getDistance())
        return self.fitness

    def getDistance(self):
        if self.distance == 0:
            tourDistance = 0
            for index in range(0, self.tourSize()):
                fromCity = self.getCity(index)
                toCity = None
                if index + 1 < self.tourSize():
                    toCity = self.getCity(index + 1)
                else:
                    toCity = self.getCity(0)
                tourDistance += fromCity.distanceTo(toCity)
            self.distance = tourDistance
        return self.distance

    def tourSize(self):
        return len(self.tour)

    def containsCity(self, city):
        if (self.tour.count(city) > 0):
            return True
        return False


class Population:
    def __init__(self, popSize, isInitial, citiesOrder):
        self.ToursList = [None] * popSize

        if isInitial:
            for tourIndex in range(0, popSize):
                tour = Tour(citiesOrder)
                tour.generateIndividual()
                self.saveTour(tourIndex, tour)

    def saveTour(self, index, tour):
        self.ToursList[index] = tour

    def getTour(self, index):
        return self.ToursList[index]

    def getFittest(self):
        fittest = self.ToursList[0]
        for index in range(1, self.popSize()):
            if fittest.getFitness() < self.getTour(index).getFitness():
                fittest = self.getTour(index)
        return fittest

    def popSize(self):
        return len(self.ToursList)


class GA:
    def __init__(self, citiesOrder):
        self.citiesOrder = citiesOrder
        self.mutationRate = 0.15
        self.tournamentSize = 5
        self.elitism = True

    def evolvePop(self, pop):
        newPop = Population(pop.popSize(), False, self.citiesOrder)
        elitismOffset = 0

        if self.elitism:
            newPop.saveTour(0, pop.getFittest())
            elitismOffset = 1

        for tourIndex in range(elitismOffset, newPop.popSize()):
            parent1 = self.tournamentSelect(pop)
            parent2 = self.tournamentSelect(pop)

            child = self.crossover(parent1, parent2)
            newPop.saveTour(tourIndex, child)

        for tourIndex in range(elitismOffset, newPop.popSize()):
            self.mutate(newPop.getTour(tourIndex))

        return newPop

    def crossover(self, parent1, parent2):
        child = Tour(self.citiesOrder)

        startPos = random.randint(0, parent1.tourSize() - 1)
        endPos = random.randint(0, parent1.tourSize() - 1)

        for cityIndex in range(0, child.tourSize()):
            if startPos < endPos and cityIndex > startPos and cityIndex < endPos:
                child.setCity(cityIndex, parent1.getCity(cityIndex))
            elif startPos > endPos:
                if not (cityIndex < startPos and cityIndex > endPos):
                    child.setCity(cityIndex, parent1.getCity(cityIndex))

        for parent2CityIndex in range(0, parent2.tourSize()):
            if not child.containsCity(parent2.getCity(parent2CityIndex)):
                for childCityIndex in range(0, child.tourSize()):
                    if child.getCity(childCityIndex) == None:
                        child.setCity(childCityIndex,
                                      parent2.getCity(parent2CityIndex))
                        break

        return child

    # Maintain genetic diversity by swap mutation
    def mutate(self, tour):
        for cityIndex in range(0, tour.tourSize()):

            # Swaps 2 cities in a tour
            if random.random() < self.mutationRate:
                randomCityIndex = random.randint(0, tour.tourSize() - 1)

                city1 = tour.getCity(cityIndex)
                city2 = tour.getCity(randomCityIndex)

                tour.setCity(randomCityIndex, city1)
                tour.setCity(cityIndex, city2)

    def tournamentSelect(self, pop):
        tournament = Population(self.tournamentSize, False, self.citiesOrder)
        for tourIndex in range(0, self.tournamentSize):
            randomTourIndex = random.randint(0, pop.popSize() - 1)
            tournament.saveTour(tourIndex, pop.getTour(randomTourIndex))
        fittest = tournament.getFittest()
        return fittest


def showPath(pop, generation):
    x = []
    y = []
    bestTour = pop.getFittest()

    for i in range(0, bestTour.tourSize()):
        city = bestTour.getCity(i)
        x.append(city.getX())
        y.append(city.getY())

    city = bestTour.getCity(0)
    x.append(city.getX())
    y.append(city.getY())
    distance = bestTour.getDistance()
    Show.show(x, y, f"Gen: {str(generation)}\nDist: {distance:.2f}")


cityLocations = [
    {
        "x": 60,
        "y": 200
    },
    {
        "x": 180,
        "y": 200
    },
    {
        "x": 80,
        "y": 180
    },
    {
        "x": 140,
        "y": 180
    },
    {
        "x": 20,
        "y": 160
    },
    {
        "x": 100,
        "y": 160
    },
    {
        "x": 200,
        "y": 160
    },
    {
        "x": 140,
        "y": 140
    },
    {
        "x": 40,
        "y": 120
    },
    {
        "x": 100,
        "y": 120
    },
    {
        "x": 180,
        "y": 100
    },
    {
        "x": 60,
        "y": 80
    },
    {
        "x": 120,
        "y": 80
    },
    {
        "x": 180,
        "y": 60
    },
    {
        "x": 20,
        "y": 40
    },
    {
        "x": 100,
        "y": 40
    },
    {
        "x": 200,
        "y": 40
    },
    {
        "x": 20,
        "y": 20
    },
    {
        "x": 60,
        "y": 20
    },
    {
        "x": 160,
        "y": 20
    },
]

cities = CityList()
for location in cityLocations:
    cities.addCity(City(location["x"], location["y"]))

pop = Population(20, True, cities)
print(f"Initial distance: {pop.getFittest().getDistance()}")

distanceList = []
ga = GA(cities)
distanceList.append(pop.getFittest().getDistance())
pop = ga.evolvePop(pop)
for generationIndex in range(0, 100000):
    pop = ga.evolvePop(pop)
    distanceList.append(pop.getFittest().getDistance())
    if generationIndex % 1000 == 0:
        showPath(pop, generationIndex)

print("Finished")
print(f"Final distance: {pop.getFittest().getDistance()}")

plt.plot(distanceList)
plt.ylabel('Distance')
plt.xlabel('Generation')
plt.show()