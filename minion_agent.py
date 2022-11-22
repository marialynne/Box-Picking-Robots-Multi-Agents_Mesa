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
        self.randomSteps = 0
        self.destinationSteps = 0
        self.boxesCount = 0
        self.index = 0
        self.stacksDirections = []
       
    def getDestinations(self):
        for y in range(0, self.model.rows):
            for x in range(0, self.model.columns):
                if (x == 0 and y == 20):
                    self.stacksDirections.append((x,y))
   
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

    def goToDestination(self, callback):
        bestDistance = math.inf
        bestNeighbor = None
        neighbors = [cell for cell in self.model.grid.get_neighborhood(self.pos, False) if self.model.grid.is_cell_empty(cell)]
        for neighbor in neighbors:
            distance = self.distanceBetweenPoints(neighbor, self.destination)
            if (distance <= bestDistance) and (not neighbor == self.prevCell): 
                bestDistance = distance
                bestNeighbor = neighbor
        self.prevCell = self.pos
        if bestNeighbor: 
            self.model.grid.move_agent(self, bestNeighbor)
            agent = self.model.grid.get_neighborhood(self.pos, False)
            if self.destination in agent: callback()
        
    def setDestination(self, destination):
        self.destination = destination

    def pickBox(self):
        self.box = self.model.grid.get_cell_list_contents([self.destination])
        if len(self.box) <= 0:
            self.box = None
            self.destination = None
            return 
        self.boxesCount += 1
        self.model.grid.remove_agent(self.box[0])
    
    def pileBox(self):
        print(self.box.pos)
        self.model.grid.place_agent(self.box, self.stacksDirections[self.index])
        self.box = None 
        self.destination = None
        
    def step(self):
        self.getDestinations()
        if not self.destination: self.randomMove()
        else:
            if not self.box: 
                self.goToDestination(self.pickBox)
            else:
                self.destination = self.stacksDirections[self.index]
                self.goToDestination(self.pileBox)
                
        mates = self.model.grid.get_cell_list_contents([self.stacksDirections[self.index]])        
        if len(mates) >= 6:
            self.index += 1