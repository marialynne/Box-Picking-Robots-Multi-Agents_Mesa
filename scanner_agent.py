import mesa
import random
import math
import numpy as np
from box_agent import BoxAgent
from wall_agent import WallAgent
from minion_agent import MinionAgent

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
        self.prevCell = []
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

        #print(list(self.destinationList))
        
    def checkIfFound(self, currentCell):
        for i in range(0, len(self.foundBoxes)):
            if currentCell == self.foundBoxes[i]:
                return True
        return False
    
    def distanceBetweenPoints(self, point1, point2):
        return math.sqrt(pow((point2[0] - point1[0]), 2) + pow((point2[1] - point1[1]), 2))

    def getToDestination(self, destination):
        neighbors = self.model.grid.get_neighborhood(self.pos, False)
        if destination in neighbors: 
            self.arrived = True
            return
        bestPoint = None
        bestDistance = math.inf
        for neighbor in neighbors:
            if self.model.grid.is_cell_empty(neighbor) and (not neighbor == self.prevCell):
                distance = self.distanceBetweenPoints(destination, neighbor)
                if distance < bestDistance:
                    bestDistance = distance
                    bestPoint = neighbor
        if (bestDistance == math.inf):
            self.prevCell = None
        else:
            self.prevCell = self.pos
            self.model.grid.move_agent(self, bestPoint)
        return
    
    def move(self):
        if self.arrived: 
            self.index += 1
            self.arrived = False
        else: self.getToDestination(self.destinationList[self.index])

    def outOfBounds(self, position):
        if position[0] >= self.model.columns: return True
        if position[0] < 0: return True
        if position[1] >= self.model.rows: return True
        if position[1] < 0: return True
        return False

    def getFieldView(self, cells):
        print('CELLS => ', cells)
        if len(cells) > 0:
            index = 0
            while(index < len(cells) and type(cells[index]) != WallAgent):
                if type(cells[index]) == BoxAgent and not cells[index] in self.foundBoxes:
                    self.foundBoxes.append(cells[index].pos)
                index += 1

        
    def searchSurroundings(self):
        northCells = []
        eastCells = []
        westCells = []
        southCells = []
        for index in range(1, self.visionRange + 1):
            northCell = (self.pos[0], self.pos[1] + index)
            eastCell = (self.pos[0] + index, self.pos[1])
            westCell = (self.pos[0] - index, self.pos[1])
            southCell = (self.pos[0], self.pos[1] - index)
            if not self.outOfBounds(northCell): northCells.append(northCell)
            if not self.outOfBounds(eastCell): eastCells.append(eastCell)
            if not self.outOfBounds(westCell): westCells.append(westCell)
            if not self.outOfBounds(southCell): southCells.append(southCell)

        print('NORTH =>', northCells)
        print('EAST =>', eastCells)
        print('WEST =>', westCells)
        print('SOUTH =>', southCells)

        print(self.model.grid.get_cell_list_contents(northCells))
        
        self.getFieldView(self.model.grid.get_cell_list_contents(northCells))
        self.getFieldView(self.model.grid.get_cell_list_contents(eastCells))
        self.getFieldView(self.model.grid.get_cell_list_contents(westCells))
        self.getFieldView(self.model.grid.get_cell_list_contents(southCells))

        print('BOXES =>', self.foundBoxes)

        """ for i in range(1, self.visionRange + 1):
            if x + i <= 20:
                currentCell = (x + i, y)
                cellmates = self.model.grid.get_cell_list_contents(currentCell)
                for j in range (0, len(cellmates)):
                    agent = cellmates[j]
                    if type(agent) == BoxAgent and not self.checkIfFound(currentCell):
                        self.foundBoxes.append(currentCell)
                    elif type(agent) == WallAgent:
                        i += 21
                        break
            else:
                break """

        """ for i in range(1, self.visionRange + 1):
            if x - i >= 0:
                currentCell = (x - i, y)
                cellmates = self.model.grid.get_cell_list_contents(currentCell)
                for j in range (0, len(cellmates)):
                    agent = cellmates[j]
                    if type(agent) == BoxAgent and not self.checkIfFound(currentCell):
                        self.foundBoxes.append(currentCell)
                    elif type(agent) == WallAgent:
                        i == -1
                        break
            else:
                break """

        """ for i in range(1, self.visionRange + 1):
            if y + i <= 20:
                currentCell = (x, y + i)
                cellmates = self.model.grid.get_cell_list_contents(currentCell)
                for j in range (0, len(cellmates)):
                    agent = cellmates[j]
                    if type(agent) == BoxAgent and not self.checkIfFound(currentCell):
                        self.foundBoxes.append(currentCell)
                    elif type(agent) == WallAgent:
                        i += 21
                        break
            else:
                break """
        
        """ for i in range(1, self.visionRange + 1):
            if y - i >= 0:
                currentCell = (x, y - i)
                cellmates = self.model.grid.get_cell_list_contents(currentCell)
                for j in range (0, len(cellmates)):
                    agent = cellmates[j]
                    if type(agent) == BoxAgent and not self.checkIfFound(currentCell):
                        self.foundBoxes.append(currentCell)
                    elif type(agent) == WallAgent:
                        i == -1
                        break
            else:
                break """
    
    def assingBox(self):
        minions = [agent for agent in self.model.schedule.agents if type(agent) == MinionAgent]
        for minion in minions:
            if minion.box == None and len(self.foundBoxes) > 0:
                minion.setDestination(self.foundBoxes[-1])
                self.foundBoxes.pop()
                 
    
    def step(self):
        if(len(self.destinationList) == 0): self.getDestinations()
        self.move()
        self.searchSurroundings()
        if(len(self.foundBoxes) > 0): self.assingBox()
        self.movements += 1
    