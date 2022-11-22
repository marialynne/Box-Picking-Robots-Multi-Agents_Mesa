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
        self.datacollector = mesa.DataCollector({
            "Minion Random Moves": WarehouseModel.minionRandomMovements,
            "Minion Destination Movements": WarehouseModel.minionDestinationMovements,
            "Minion 1 Total Piled Boxes": lambda model: WarehouseModel.boxesPerMinion(model),
            "Minion 2 Total Piled Boxes": lambda model: WarehouseModel.boxesPerMinion(model, 2),
            "Minion 3 Total Piled Boxes": lambda model: WarehouseModel.boxesPerMinion(model, 3),
            "Minion 4 Total Piled Boxes": lambda model: WarehouseModel.boxesPerMinion(model, 4),
            "Minion 5 Total Piled Boxes": lambda model: WarehouseModel.boxesPerMinion(model, 5),
        })

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
        self.datacollector.collect(self)

    @staticmethod
    def mainRobotMovements(model) -> int: # See if it works with main robot
        #mainRobot = [agent for agent in model.schedule.agents if type(agent) == MainRobotAgent]
        #return mainRobot.steps
        return

    @staticmethod
    def minionRandomMovements(model) -> int: 
        minions = [agent for agent in model.schedule.agents if type(agent) == MinionAgent]
        totalRandomSteps = 0
        for minion in minions:
            totalRandomSteps += minion.randomSteps 
        return totalRandomSteps

    @staticmethod
    def minionDestinationMovements(model) -> int:
        minions = [agent for agent in model.schedule.agents if type(agent) == MinionAgent]
        totalDestinationSteps = 0
        for minion in minions:
            totalDestinationSteps += minion.destinationSteps
        return totalDestinationSteps

    @staticmethod
    def boxesPerMinion(model, minion = 1) -> int: 
        minion = [agent for agent in model.schedule.agents if type(agent) == MinionAgent][minion]
        return minion.boxesCount

    @staticmethod
    def percentagePiledBoxes(model) -> int: 
        return 1