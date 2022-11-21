import mesa
import random
from wall_agent import WallAgent
from box_agent import BoxAgent
from minion_agent import MinionAgent
from stack_agent import StackAgent

class WarehouseModel(mesa.Model):     
    def __init__(self, walls, boxes, time):
        self.schedule = mesa.time.RandomActivationByType(self)
        self.running = True
        self.current_id = 0
        self.walls = walls
        self.boxes = boxes
        rows = 21
        columns = 21
        self.time = time
        self.grid = mesa.space.MultiGrid(rows, columns, False)
        #agentTypes = [WallAgent, WallAgent, BoxAgent, BoxAgent, BoxAgent]
        agentTypes = [WallAgent, WallAgent, WallAgent, WallAgent]

        # Add only one minion
        agent = MinionAgent(self.next_id(), self)
        agent.setDestination((15, 18))
        self.addAgent(agent,0,0)
        agent = MinionAgent(self.next_id(), self)
        agent.setDestination((10, 10))
        self.addAgent(agent,0,0)
        agent = MinionAgent(self.next_id(), self)
        agent.setDestination((4, 18))
        self.addAgent(agent,0,0)
        agent = MinionAgent(self.next_id(), self)
        agent.setDestination((5, 8))
        self.addAgent(agent,0,0)
        
        agent = BoxAgent(self.next_id(), self)
        self.addAgent(agent,15,18)
        agent = BoxAgent(self.next_id(), self)
        self.addAgent(agent,10,10)
        agent = BoxAgent(self.next_id(), self)
        self.addAgent(agent,4,18)
        agent = BoxAgent(self.next_id(), self)
        self.addAgent(agent,5,8)

        for _ in range(self.walls):
            index = random.randrange(len(agentTypes))
            agent = WallAgent(self.next_id(), self)
            
            if type(agent) == MinionAgent: agent.setDestination((10, 10))
            self.schedule.add(agent)
            emptyCell = self.grid.find_empty()
            while emptyCell[1] >= 18: emptyCell = self.grid.find_empty()
            self.grid.place_agent(agent, emptyCell)

            for index in range(0, agent.width):
                neighborCell = random.choice(self.grid.get_neighborhood(emptyCell, False))
                while not self.grid.is_cell_empty(neighborCell):
                    neighborCell = random.choice(self.grid.get_neighborhood(emptyCell, False))
                nextAgent = agentTypes[index](self.next_id(), self, agent.width)
                self.grid.place_agent(nextAgent, neighborCell)
                emptyCell = neighborCell
                
    def addAgent(self, agent, row, col) -> None:
        self.schedule.add(agent)
        self.grid.place_agent(agent,(row, col))
      
    def run_model(self) -> None:
        while self.running:
            self.step()
            
    def next_id(self) -> int:
        self.current_id += 1
        return self.current_id

    def step(self):
        self.schedule.step()