import mesa
import random

class MinionAgent(mesa.Agent):     
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 2
        self.width = 1
        self.prevCells = []
        self.destination = None

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

    def step(self):
        if not self.destination: self.randomMove()
        return