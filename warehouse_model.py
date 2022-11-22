import mesa
import random
from wall_agent import WallAgent
from box_agent import BoxAgent
from minion_agent import MinionAgent
from stack_agent import StackAgent
from scanner_agent import ScannerAgent

class WarehouseModel(mesa.Model):     
    def __init__(self, walls, boxes, visionRange, time):
        self.schedule = mesa.time.RandomActivationByType(self)
        self.running = True
        self.current_id = 0
        self.walls = walls
        self.boxes = boxes
        rows = 21
        columns = 21
        hallwayWidth = 3
        minions = 4
        self.time = time
        self.grid = mesa.space.MultiGrid(rows, columns, False)
        # agentTypes = [WallAgent, WallAgent, BoxAgent, BoxAgent, BoxAgent]
        agentTypes = [WallAgent, WallAgent, WallAgent, WallAgent]

        #Add Scanner Agent
        agent = ScannerAgent(self.next_id(), visionRange, self)
        self.grid.place_agent(agent, (20, 19))

        for _ in range(self.walls):
            agent = WallAgent(self.next_id(), self)
            emptyCell = self.grid.find_empty()
            while (emptyCell[1] >= ((rows-1) - hallwayWidth)) and self.haveNeighbors(emptyCell):  emptyCell = self.grid.find_empty()
            self.grid.place_agent(agent, emptyCell)
            # self.haveNeighbors(emptyCell)
        
        for _ in range(self.boxes + minions):
            emptyCell = self.grid.find_empty()
            while (emptyCell[1] >= ((rows-1) - hallwayWidth)):  emptyCell = self.grid.find_empty()
            if self.boxes > 0:
                agent = BoxAgent(self.next_id(), self)
                self.addAgent(agent,emptyCell[0],emptyCell[1])
                self.boxes-=1
            else:
                agent = MinionAgent(self.next_id(), self)
                self.addAgent(agent,emptyCell[0],emptyCell[1])
        
        for col in range(0,columns):
            agent = StackAgent(self.next_id(), self)
            self.addAgent(agent,col,rows-1)
                
    def addAgent(self, agent, row, col) -> None:
        self.schedule.add(agent)
        self.grid.place_agent(agent,(row, col))
    
    def haveNeighbors(self, emptyCell):
        neighbors = self.grid.get_neighborhood(emptyCell, True)
        hasNeighbor = filter(lambda cell: not self.grid.is_cell_empty(cell), neighbors)
        if len(list(hasNeighbor)) == 0: return True
        else: return False
    
    def run_model(self) -> None:
        while self.running:
            self.step()
            
    def next_id(self) -> int:
        self.current_id += 1
        return self.current_id

    def step(self):
        self.schedule.step()