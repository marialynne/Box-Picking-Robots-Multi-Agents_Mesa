import mesa

class StackAgent(mesa.Agent):     
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 4
      
    def step(self):
        pass

