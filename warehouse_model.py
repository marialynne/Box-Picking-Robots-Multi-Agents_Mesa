import mesa
import random
from wall_agent import WallAgent
from box_agent import BoxAgent
from minion_agent import MinionAgent
from stack_agent import StackAgent

class WarehouseModel(mesa.Model):     
    def __init__(self, agents, time):
        self.schedule = mesa.time.RandomActivationByType(self)
        self.running = True
        self.agents = agents
        rows = 21
        columns = 21
        self.time = time
        self.id = 0
        self.grid = mesa.space.MultiGrid(rows, columns, False)
        # agentTypes = [WallAgent, WallAgent, BoxAgent, BoxAgent, BoxAgent]
        agentTypes = [WallAgent, WallAgent, WallAgent, WallAgent]
        self.datacollector = mesa.DataCollector({
            "Minion Random Moves": WarehouseModel.minionRandomMovements,
            "Minion Destination Movements": WarehouseModel.minionDestinationMovements,
        })

        # Add only one minion
        agent = MinionAgent(self.id, self)
        agent.setDestination((15, 18))
        self.schedule.add(agent)
        self.grid.place_agent(agent, (0, 0))
        self.id += 1
    
        agent = BoxAgent(self.id, self)
        self.schedule.add(agent)
        self.grid.place_agent(agent, (10, 10))
        self.id += 1

        for _ in range(self.agents):
            index = random.randrange(len(agentTypes))
            agent = agentTypes[index](self.id, self)
            if type(agent) == MinionAgent: agent.setDestination((10, 10))
            self.schedule.add(agent)
            emptyCell = self.grid.find_empty()
            self.grid.place_agent(agent, emptyCell)
            self.id += 1

            for index in range(0, agent.width):
                neighborCell = random.choice(self.grid.get_neighborhood(emptyCell, False))
                while not self.grid.is_cell_empty(neighborCell):
                    neighborCell = random.choice(self.grid.get_neighborhood(emptyCell, False))
                nextAgent = agentTypes[index](self.id, self, agent.width)
                self.grid.place_agent(nextAgent, neighborCell)
                emptyCell = neighborCell
                self.id += 1
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
        return 1

    @staticmethod
    def percentagePiledBoxes(model) -> int: 
        return 1