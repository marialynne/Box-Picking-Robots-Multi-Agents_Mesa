import mesa
import random
import math
from box_agent import BoxAgent

class MinionAgent(mesa.Agent):     
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 2
        self.width = 1
        self.prevCells = []
        self.box = None
        self.stepsToDestination = 0
        self.destination = None

    def mantainPrevCells(self):
        while len(self.prevCells) >= 25:
            self.prevCells.pop()#

    def randomMove(self):
        neighborCell = random.choice(self.model.grid.get_neighborhood(self.pos, False))
        while not self.model.grid.is_cell_empty(neighborCell) and (not neighborCell in self.prevCells):
            neighborCell = random.choice(self.model.grid.get_neighborhood(self.pos, False))
        self.prevCells.append(neighborCell)
        self.model.grid.move_agent(self, neighborCell)
        self.mantainPrevCells()
    
    def distanceBetweenPoints(self, point1, point2):
        return math.sqrt(pow((point2[0] - point1[0]), 2) + pow((point2[1] - point1[1]), 2))

    def getToDestination(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, False)
        if self.destination in neighbors: return True
        bestPoint = None
        bestDistance = -1
        for neighbor in neighbors:
            if self.model.grid.is_cell_empty(neighbor) and (not neighbor in self.prevCells) and neighbor[1] <= 19:
                distance = self.distanceBetweenPoints(self.destination, neighbor)
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

    def setDestination(self, destination):
        self.destination = destination

    def pickBox(self):
        box = self.model.grid.get_cell_list_contents([self.destination])
        if len(box) > 0:
            box = box[0]
            self.box = box
            self.model.grid.remove_agent(box)
            self.destination = (0, 20)
            self.stepsToDestination = 0

    def pileBox(self):
        while len(self.model.grid.get_cell_list_contents([self.destination])) >= 5:
            self.destination = (self.destination[0] + 1, self.destination[1])
            self.getToDestination()
        self.model.grid.place_agent(self.box, self.destination)
        self.stepsToDestination = 0
        self.box = None
        self.prevCells = []
        self.destination = None

    def step(self):
        if not self.destination: 
            self.randomMove()
        else:
            if self.stepsToDestination == 0: self.prevCells = []
            if self.getToDestination(): self.pickBox()
            if self.pos[1] >= 19 and self.pos[0] == self.destination[0]: self.pileBox()
        pass