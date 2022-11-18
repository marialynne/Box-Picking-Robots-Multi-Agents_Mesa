from bootleg_model import *
import matplotlib.pyplot as plt
import pandas as pd
from mesa.visualization.UserParam import UserSettableParameter

PIXELS_GRID = 500

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true"}
    if agent.type == 2: # Robot
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.8
    elif agent.type == 1: # Box
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 1
        portrayal["h"] = 1
        portrayal["w"] = 1
    else: # Walls
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
        portrayal["h"] = 1
        portrayal["w"] = 1
    return portrayal

simulation_params = {
    "agents": UserSettableParameter(
        "slider",
        "Number of Agents",
        value=15,
        min_value=1,
        max_value=30,
        step=1,
        description="Number of Agents",
    ),
    "time": UserSettableParameter(
        "number",
        "Time",
        25,
        description="Time to end",
    )
}

grid = mesa.visualization.CanvasGrid(
    agent_portrayal, 21, 21, 600, 600)

server = mesa.visualization.ModularServer(
    BootlegModel, [
        grid], "Bootleg", simulation_params
)

server.port = 853
server.launch()
