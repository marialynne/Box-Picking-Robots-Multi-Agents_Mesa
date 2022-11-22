import mesa
import random
import math
from box_agent import BoxAgent
from stack_agent import StackAgent
class MinionAgent(mesa.Agent):     
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 2
        self.width = 1
        self.prevCells = []
        self.prevCell = None
        self.box = None
        self.stepsToDestination = 0
        self.destination = None
        self.goToPile = False
        self.randomSteps = 0
        self.destinationSteps = 0
        self.boxesCount = 0

    def mantainPrevCells(self):
        while len(self.prevCells) >= 25:
            self.prevCells.pop()

    def randomMove(self):
        neighborCell = random.choice(self.model.grid.get_neighborhood(self.pos, False))
        while not self.model.grid.is_cell_empty(neighborCell) and (not neighborCell in self.prevCells):
            neighborCell = random.choice(self.model.grid.get_neighborhood(self.pos, False))
        self.prevCells.append(neighborCell)
        self.model.grid.move_agent(self, neighborCell)
        self.mantainPrevCells()
        self.randomSteps += 1
    
    def distanceBetweenPoints(self, point1, point2):
        return math.sqrt(pow((point2[0] - point1[0]), 2) + pow((point2[1] - point1[1]), 2))

    def getToDestination(self, callback):
        """ bestDistance = math.inf
        bestNeighbor = None
        neighbors = neighbors = self.model.grid.get_neighborhood(self.pos, False)
        if self.destination in neighbors: callback()
        for neighbor in neighbors:
            if self.model.grid.is_cell_empty(neighbor) and (not neighbor == self.prevCell):
                distance = self.distanceBetweenPoints(neighbor, self.destination)
                if (distance <= bestDistance): 
                    bestDistance = distance
                    bestNeighbor = neighbor
        self.prevCell = self.pos
        self.model.grid.move_agent(self, bestNeighbor) """
        neighbors = self.model.grid.get_neighborhood(self.pos, False)
        if self.destination in neighbors: return callback()
        bestPoint = None
        bestDistance = math.inf
        for neighbor in neighbors:
            if self.model.grid.is_cell_empty(neighbor) and (not neighbor == self.prevCell):
                distance = self.distanceBetweenPoints(self.destination, neighbor)
                if distance < bestDistance:
                    bestDistance = distance
                    bestPoint = neighbor
        if (bestDistance == math.inf):
            self.prevCell = None
        else:
            self.prevCell = self.pos
            self.model.grid.move_agent(self, bestPoint)
            return


    def setDestination(self, destination):
        self.destination = destination

    def pickBox(self):
        box = self.model.grid.get_cell_list_contents([self.destination])
        if len(box) > 0 and type(box[0]) == BoxAgent:
            self.box = box[0]
            self.model.grid.remove_agent(self.box)
            self.destination = (0, self.model.rows - 1)
            self.boxesCount += 1
        else: self.destination = None

    def getPile(self):
        while len(self.model.grid.get_cell_list_contents([self.destination])) >= 5:
            self.destination = (self.destination[0] + 1, self.destination[1])
        self.goToPile = True

    def pileBox(self):
        if self.box != None:
            self.model.grid.place_agent(self.box, self.destination)
            self.box = None
            self.prevCells = []
            self.destination = None
            self.goToPile = False
        else:
            self.goToPile = False
            self.destination = None

    def step(self):
        if not self.destination: 
            self.randomMove()
        else:
            if not self.box: self.getToDestination(self.pickBox)
            elif self.box and self.goToPile: self.getToDestination(self.pileBox)
            elif self.box: 
                self.getToDestination(self.getPile)
        pass