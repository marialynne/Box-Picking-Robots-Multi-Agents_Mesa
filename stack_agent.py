import mesa

class StackAgent(mesa.Agent):     
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 4
        self.boxes = 0
        self.listBoxes = []
    
    def addBox(self, box):
        self.boxes += 1
        self.listBoxes.append(box)
      
    def step(self):
        pass

