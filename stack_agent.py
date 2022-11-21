import mesa
import random

class StackAgent(mesa.Agent):     
    def __init__(self, unique_id, model, width = random.randrange(1, 3, 1)):
        super().__init__(unique_id, model)
        self.type = 0
        self.width = width

    def step(self):
        return

