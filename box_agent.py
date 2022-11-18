import mesa

class BoxAgent(mesa.Agent):     
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 1
        self.width = 1

    def step(self):
        return