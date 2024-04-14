from warehouse.agents import *
from .constants import *

def warehouse_portrayal(agent):
   """
   Determine which portrayal to use according to the type of agent.
   """
   if isinstance(agent,PickerRobot):
        return robot_portrayal(agent)
   elif isinstance(agent,Box):
        return box_portrayal(agent)
   elif isinstance(agent,Rack):
       return rack_portrayal(agent)
   else:
       return tile_portrayal(agent)
       

def robot_portrayal(robot):

    imgs = {(FREE,*UP):"img/robot1-up.png",(FREE,*DOWN):"img/robot1-down.png",(FREE,*LEFT):"img/robot1-left.png",(FREE,*RIGHT):"img/robot1-right.png",(BUSY,*UP):"img/robot1-busy-up.png",(BUSY,*DOWN):"img/robot1-busy-down.png",(BUSY,*LEFT):"img/robot1-busy-left.png",(BUSY,*RIGHT):"img/robot1-busy-right.png"}

    if robot is None:
        raise AssertionError
    return {
        "Shape": imgs[(robot.load_state,*robot.direction)] ,
        "w": 1,
        "h": 1,
        "Layer": 2,
        "x": robot.x,
        "y": robot.y,
        "scale": 1.5,
    }

def box_portrayal(box):

    if box is None:
        raise AssertionError
    return {
        "Shape": "img/boxes.png",
        "w": 1,
        "h": 1,
        "Layer": 1,
        "x": box.x,
        "y": box.y,
    }

def rack_portrayal(rack):

    if rack is None:
        raise AssertionError
    return {
        "Shape": "img/rack.png",
        "w": 1,
        "h": 1,
        "scale": 1.5,
        "Layer": 1,
        "x": rack.x,
        "y": rack.y,
    }
def tile_portrayal(tile):
    if tile is None:
        raise AssertionError
    return {
        "Shape": "img/tile_selected.png" if tile.is_target else "img/tile_empty.png",
        "scale": 1,
        "Layer": 0,
        "x": tile.x,
        "y": tile.y,
    }