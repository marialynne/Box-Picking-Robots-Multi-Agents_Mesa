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

    def getToDestination(self):
        bestDistance = math.inf
        bestNeighbor = None
        neighbors = [cell for cell in self.model.grid.get_neighborhood(self.pos, False) if self.model.grid.is_cell_empty(cell)]
        print(neighbors, '  ', self.destination)
        for neighbor in neighbors:
            distance = self.distanceBetweenPoints(neighbor, self.destination)
            if (distance <= bestDistance) and (not neighbor == self.prevCell): 
                bestDistance = distance
                bestNeighbor = neighbor
        print(bestNeighbor)
        self.prevCell = self.pos
        self.model.grid.move_agent(self, bestNeighbor)
        newNeighbors = self.model.grid.get_neighborhood(self.pos, False)
        if self.destination in newNeighbors: self.pickBox()

        """ neighbors = self.model.grid.get_neighborhood(self.pos, False)
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
            self.destinationSteps += 1
            self.prevCells.append(bestPoint)
            self.stepsToDestination += 1
            self.model.grid.move_agent(self, bestPoint)
        return False """

    def setDestination(self, destination):
        self.destination = destination

    def pickBox(self):
        box = self.model.grid.get_cell_list_contents([self.destination])
        if len(box) > 0:
            self.box = box[0]
            self.model.grid.remove_agent(self.box)
            self.destination = (0, self.model.rows)
            # self.stepsToDestination = 0
            self.boxesCount += 1

    def pileBox(self):
        stack = [agent for agent in self.model.grid.get_cell_list_contents([self.destination]) if type(agent) == StackAgent]
        print(stack)
        if len(stack) > 0:
            while stack[0].boxes >= 5:
                self.destination = (self.destination[0] + 1, self.destination[1])
                stack = self.model.grid.get_cell_list_contents([self.destination])
                self.getToDestination()
            stack[0].addBox(self.box)
            if self.box != None:
                self.model.grid.place_agent(self.box, self.destination)
                self.stepsToDestination = 0
                self.box = None
                self.prevCells = []
                self.destination = None

    def step(self):
        if not self.destination: 
            self.randomMove()
        else:
            self.getToDestination()
            """ if self.stepsToDestination == 0: self.prevCells = []
            if self.getToDestination(): self.pickBox()
            if self.pos[1] >= 19 and self.pos[0] == self.destination[0]: self.pileBox() """
        pass