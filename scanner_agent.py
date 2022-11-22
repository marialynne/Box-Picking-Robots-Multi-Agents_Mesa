import mesa
import random

from box_agent import BoxAgent
from wall_agent import WallAgent

class ScannerAgent(mesa.Agent):     
    def __init__(self, unique_id, visionRange, model):
        super().__init__(unique_id, model)
        self.type = 3
        self.width = 1
        self.direction = 0
        self.dirVariation = [0, 0]
        self.visionRange = visionRange
        self.visited = []
        self.foundBoxes = []
    
    def moveRandom(self):
        x, y = self.pos
        if y >= 1 and y <= 19:
            if self.model.grid.is_cell_empty((x, y - 1)):
                self.model.grid.move_agent(self, (x, y - 1))
            elif self.direction == 0 and self.model.grid.is_cell_empty((x + 1, y)):
                self.model.grid.move_agent(self, (x + 1, y))
        elif x >= 1 and x <= 19:
            if self.direction == 1 and self.model.grid.is_cell_empty((x - 1, y)):
                self.model.grid.move_agent(self, (x - 1, y))
            else:
                self.model.grid.move_agent(self, (x, y + 1))
        newX, newY = self.pos
        if newY > y:
            self.dirVariation[1] += (newY - y)
        elif y > newY:
            self.dirVariation[1] -= (y - newY)
        '''x, y = self.pos
        neigborCells = self.model.grid.get_neighborhood(self.pos, False)
        for i in range (0, len(neigborCells)):
            neighborCell = neigborCells[i]
            if self.model.grid.is_cell_empty(neighborCell) and not self.alreadyVisited(neighborCell) and i < len(neigborCells):
                self.model.grid.move_agent(self, neighborCell)
                newX, newY = self.pos
                if newY > y:
                    self.dirVariation[1] += (newY - y)
                elif y > newY:
                    self.dirVariation[1] -= (y - newY)
                return
        neighborCell = random.choice(self.model.grid.get_neighborhood(self.pos, False))
        while not self.model.grid.is_cell_empty(neighborCell):
            neighborCell = random.choice(self.model.grid.get_neighborhood(self.pos, False))
        self.model.grid.move_agent(self, neighborCell)
        newX, newY = self.pos
        if newY > y:
            self.dirVariation[1] += (newY - y)
        elif y > newY:
            self.dirVariation[1] -= (y - newY)
        self.visited.pop(len(self.visited) - 1)
        self.visited.pop(len(self.visited) - 1)
        self.visited.pop(len(self.visited) - 1)
        self.visited.pop(len(self.visited) - 1)'''
        '''self.visited.pop(len(self.visited) - 1)
        self.visited.pop(len(self.visited) - 1)
        self.visited.pop(len(self.visited) - 1)
        self.visited.pop(len(self.visited) - 1)'''
        ''' neighborCell = random.choice(self.model.grid.get_neighborhood(self.pos, False))
        while not self.model.grid.is_cell_empty(neighborCell): #or self.alreadyVisited(neighborCell):
            neighborCell = random.choice(self.model.grid.get_neighborhood(self.pos, False))
        self.model.grid.move_agent(self, neighborCell)'''

    def movementNotPossible(self):
        x, y = self.pos
        if x >= 1 and x <= 19:
            if not self.alreadyVisited((x + 1, y)) and self.model.grid.is_cell_empty((x + 1, y)):
                return True
            elif not self.alreadyVisited((x - 1, y)) and self.model.grid.is_cell_empty((x - 1, y)):
                return True

        if  y >= 1 and y <= 19:
            if not self.alreadyVisited((x, y + 1)) and self.model.grid.is_cell_empty((x, y + 1)):
             return True
            elif not self.alreadyVisited((x, y - 1)) and self.model.grid.is_cell_empty((x, y - 1)):
                return True

        return False


    def checkIfFound(self, currentCell):
        for i in range(0, len(self.foundBoxes)):
            if currentCell == self.foundBoxes[i]:
                return True
        return False

    def returnToDir(self):
        x, y = self.pos
        if self.dirVariation[1] > 0 and self.model.grid.is_cell_empty((x, y - 1)) and not self.alreadyVisited((x, y - 1)):
            self.model.grid.move_agent(self, (x, y - 1))
            self.dirVariation[1] -= 1
        elif self.dirVariation[1] < 0 and self.model.grid.is_cell_empty((x, y + 1)) and not self.alreadyVisited((x, y + 1)):
            self.model.grid.move_agent(self, (x, y + 1))
            self.dirVariation[1] += 1
        else:
            self.move()


    def searchSurroundings(self):
        x,y = self.pos
        for i in range(1, self.visionRange + 1):
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
                break

        for i in range(1, self.visionRange + 1):
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
                break

        for i in range(1, self.visionRange + 1):
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
                break
        
        for i in range(1, self.visionRange + 1):
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
                break

    def alreadyVisited(self, nextCell):
        for i in range(0, len(self.visited)):
            if(nextCell == self.visited[i]):
                return True
        return False

    def move(self):
        x,y = self.pos

        if not self.movementNotPossible():
            self.alreadyVisited.clear()
            self.moveRandom()
        elif x > 0 and self.direction == 0 and not self.alreadyVisited((x - 1, y)):
            nextCell = (x - 1, y)
            if self.model.grid.is_cell_empty(nextCell):
                self.model.grid.move_agent(self, nextCell)
            else:
                self.moveRandom()
        elif x == 0 and self.direction == 0:
            nextCell = (x, y - 1)
            if self.model.grid.is_cell_empty(nextCell):
                self.model.grid.move_agent(self, nextCell)
                self.direction = 1
            else:
                self.moveRandom()
                self.direction = 1
        elif x < 20 and self.direction == 1 and not self.alreadyVisited((x + 1, y)):
            nextCell = (x + 1, y)
            if self.model.grid.is_cell_empty(nextCell):
                self.model.grid.move_agent(self, nextCell)
            else:
                self.moveRandom()
        elif x == 20 and self.direction == 1:
            nextCell = (x, y - 1)
            if self.model.grid.is_cell_empty(nextCell):
                self.model.grid.move_agent(self, nextCell)
                self.direction = 0
            else:
                self.moveRandom()
                self.direction = 0
        else:
            self.moveRandom()
        
        self.visited.append(self.pos)
  
    def printFound(self):
        print("Found:")
        for i in range (0, len(self.foundBoxes)):
            print(self.foundBoxes[i])

    def step(self):
        self.searchSurroundings()
        self.printFound()
        if self.dirVariation[1] <= 1 or self.dirVariation[1] >= 1:
            self.returnToDir()
        else:
            self.move()
        return