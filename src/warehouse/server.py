
import mesa
from warehouse.model import Warehouse
from .portrayal import warehouse_portrayal
from .agents import NUMBER_OF_CELLS

SIZE_OF_CANVAS_IN_PIXELS_X = 500
SIZE_OF_CANVAS_IN_PIXELS_Y = 500

# TODO Add a parameter named "n_boxes" for the number of boxes to include in the model.
simulation_params = {
    "height": NUMBER_OF_CELLS, 
    "width": NUMBER_OF_CELLS,
    "n_robots": mesa.visualization.Slider(
        'number of robots',
        1, #default
        1, #min
        10, #max
        1, #step
        "choose how many robots to include in the simulation"
    )
    ,
    "n_boxes": 
        mesa.visualization.Slider(
        'number of boxes',
        5, #default
        1, #min
        20, #max
        1, #step
        "choose how many boxes to include in the simulation",
        
    )

    }
grid = mesa.visualization.CanvasGrid(warehouse_portrayal, NUMBER_OF_CELLS, NUMBER_OF_CELLS, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)


server = mesa.visualization.ModularServer(
    Warehouse, [grid], "Automated Warehouse", simulation_params
)