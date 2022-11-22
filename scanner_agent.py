import mesa
import random
import math
import numpy as np
from box_agent import BoxAgent
from wall_agent import WallAgent

class ScannerAgent(mesa.Agent):     
    def __init__(self, unique_id, model, visionRange, rows, columns):
        super().__init__(unique_id, model)
        self.type = 3
        self.visionRange = visionRange
        self.rows = rows
        self.columns = columns
        self.foundBoxes = []
        self.movements = 0
        self.destinationList = []
        self.prevCells = []
        self.stepsToDestination = 0
        self.arrived = False
        self.index = 0

    def getDestinations(self):
        for y in range(0, self.rows):
            for x in range(0, self.columns):
                if ((x == 0) or (x == self.columns-1) or (y == 0) or (y == self.rows)) and self.model.grid.is_cell_empty((x,y)): 
                    self.destinationList.append((x,y))
        
        random.shuffle(self.destinationList)
        
        for index,value in enumerate(self.destinationList):
            if index%2 != 0: self.destinationList.insert(index,(10,8))

        print(list(self.destinationList))
        
    
    def distanceBetweenPoints(self, point1, point2):
        return math.sqrt(pow((point2[0] - point1[0]), 2) + pow((point2[1] - point1[1]), 2))

    def getToDestination(self, destination):
        neighbors = self.model.grid.get_neighborhood(self.pos, False)
        if destination in neighbors: return True
        bestPoint = None
        bestDistance = -1
        for neighbor in neighbors:
            if self.model.grid.is_cell_empty(neighbor) and (not neighbor in self.prevCells) and neighbor[1] <= 19:
                distance = self.distanceBetweenPoints(destination, neighbor)
                if distance < bestDistance or bestDistance < 0:
                    bestDistance = distance
                    bestPoint = neighbor
        if (bestDistance < 0): 
            if len(self.prevCells) > 0: self.prevCells = [self.prevCells[-1]]
        else:
            self.prevCells.append(bestPoint)
            self.stepsToDestination += 1
            self.model.grid.move_agent(self, bestPoint)
        return False
    
    def move(self):
        if self.getToDestination(self.destinationList[self.index]): self.index+=1
    
    def step(self):
        if(len(self.destinationList) == 0): self.getDestinations()
        self.move()
        print(self.destinationList[self.index])
        pass