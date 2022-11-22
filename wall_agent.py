import mesa
import random

class WallAgent(mesa.Agent):     
    def __init__(self, unique_id, model, width = random.randint(1, 2)):
        super().__init__(unique_id, model)
        self.type = 0
        self.width = width

    def step(self):
        return

