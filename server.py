import mesa
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from warehouse_model import WarehouseModel
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule, CanvasGrid
PIXELS_GRID = 600

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true"}
    if agent.type == 5: # Stack
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "sienna"
        portrayal["Layer"] = 0
        portrayal["h"] = 1
        portrayal["w"] = 1
    elif agent.type == 4: # Empty Stack
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "peru"
        portrayal["Layer"] = 0
        portrayal["h"] = 1
        portrayal["w"] = 1
    elif agent.type == 3: # Main Robot
        portrayal["Color"] = "darkviolet"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.8
    elif agent.type == 2: # Minion
        portrayal["Color"] = "gold"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
    elif agent.type == 1: # Box
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "seagreen"
        portrayal["Layer"] = 1
        portrayal["h"] = 0.6
        portrayal["w"] = 0.6
    else: # Walls
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
        portrayal["h"] = 1
        portrayal["w"] = 1
    return portrayal

simulation_params = {
    "walls": UserSettableParameter(
        "slider",
        "Number of walls",
        value=20,
        min_value=1,
        max_value=30,
        step=1,
        description="Number of Agents",
    ),
    "boxes": UserSettableParameter(
        "slider",
        "Number of boxes",
        value=5,
        min_value=1,
        max_value=20,
        step=1,
        description="Number of Agents",
    ),
    "time": UserSettableParameter(
        "number",
        "Time",
        100,
        description="Time to end",
    )
}

# Charts
minionMovements_random = ChartModule([{"Label": "Minion Random Moves", "Color": "Blue"}], data_collector_name='datacollector')
minionMovements_destination = ChartModule([{"Label": "Minion Destination Movements", "Color": "Red"}], data_collector_name='datacollector')

grid = CanvasGrid(agent_portrayal, 21, 21, PIXELS_GRID, PIXELS_GRID)

server = mesa.visualization.ModularServer(
    WarehouseModel, [
        grid,
        minionMovements_random,
        minionMovements_destination], 
    "WarehouseModel", simulation_params
)

server.port = 853
server.launch()
