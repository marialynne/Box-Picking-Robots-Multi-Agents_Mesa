import mesa
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from warehouse_model import WarehouseModel
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule, CanvasGrid
PIXELS_GRID = 600

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true"}

    if agent.type == 4: # Stack
        #if agent.boxes < 5: 
        #else: portrayal["Color"] = "peru"
        portrayal["Color"] = "sienna"
        portrayal["Shape"] = "rect"
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
        value=1,
        min_value=5,
        max_value=25,
        step=1,
        description="Number of boxes",
    ),
    "visionRange": UserSettableParameter(
        "slider",
        "Scanner Range of Vision",
        value=5,
        min_value=1,
        max_value=10,
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
scannerAgentMovements = ChartModule([{ "Label": "Scanner Agent Moves", "Color": "Blue" }], data_collector_name='datacollector')
minionMovements_random = ChartModule([{ "Label": "Minion Random Moves", "Color": "Blue" }], data_collector_name='datacollector')
minionMovements_destination = ChartModule([ {"Label": "Minion Destination Movements", "Color": "Red" }], data_collector_name='datacollector')
minion1_boxes = ChartModule([ {"Label": "Minion 1 Total Piled Boxes", "Color": "Red" }], data_collector_name='datacollector')
minion2_boxes = ChartModule([ {"Label": "Minion 2 Total Piled Boxes", "Color": "Red" }], data_collector_name='datacollector')
minion3_boxes = ChartModule([ {"Label": "Minion 3 Total Piled Boxes", "Color": "Red" }], data_collector_name='datacollector')
minion4_boxes = ChartModule([ {"Label": "Minion 4 Total Piled Boxes", "Color": "Red" }], data_collector_name='datacollector')
minion5_boxes = ChartModule([ {"Label": "Minion 5 Total Piled Boxes", "Color": "Red" }], data_collector_name='datacollector')
percentagePiled = ChartModule([ {"Label": "Percentage piled boxes", "Color": "Blue" }], data_collector_name='datacollector')

grid = CanvasGrid(agent_portrayal, 21, 21, PIXELS_GRID, PIXELS_GRID)

server = mesa.visualization.ModularServer(
    WarehouseModel, [
        grid,
        scannerAgentMovements,
        minionMovements_random,
        minionMovements_destination,
        minion1_boxes,
        minion2_boxes,
        minion3_boxes,
        minion4_boxes,
        minion5_boxes,
        percentagePiled], 
    "WarehouseModel", simulation_params
)

# Batch run
def createPlot(results, dataValue, columns = []):
    results_df = pd.DataFrame(results)
    resultingDataFrame = pd.DataFrame(results_df, columns=[dataValue])
    print(resultingDataFrame)
    results_filtered = resultingDataFrame[(results_df.Step == 50)] # get last step resutls - TODO: CHANGE
    results_filtered.plot('iteration', dataValue)
    plt.show()
    
results = mesa.batch_run(
    WarehouseModel,
    parameters={ "walls": range(3, 25), "boxes": range(5, 20), "time": 200 , "visionRange": range(3, 5)},
    iterations=10,
    max_steps=250,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
) 

print(results)

createPlot(results, 'Minion Random Moves', ['iteration', 'Minion Random Moves'])
plt.show()


server.port = 2005
# server.launch()