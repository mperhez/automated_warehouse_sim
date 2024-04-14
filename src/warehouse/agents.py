import mesa
import numpy as np
from .constants import *    


class PickerRobot(mesa.Agent):
    """Represents a Picker Robot of the warehouse."""

    def __init__(self, id, pos, model, direction=DOWN):
        super().__init__(id, model)
        self.x, self.y = pos

        self.load_state = FREE
        self.payload = []
        self.direction = direction  # direction the robot is facing
        
        
    @property
    def isBusy(self):
        """
        Robot's state is busy if it has a payload.
        """
        return self.load_state == BUSY

    def step(self):
        """
        The robot's step function. It will make robot work for one time step.
        """
        
        action_name, kwargs = self.make_decision(self.read_mv())
        action = getattr(self,action_name )
        action(**kwargs)
        
    
    # Decision-making functions

    def make_decision(self, mv_sensor):
        """
        The robot's decision-making function. It will make robot to decide what to do based on the sensor data.
        """
        return "wait", {}
        
    
    # Simulated robot actions

    def wait(self,**kwargs):
        """
        Robot waits for the next command.
        """
        pass

    def turn(self, **kwargs):
        """
        Turns the robot's direction clockwise or counter clockwise.
        """
        clockwise = True if "clockwise" not in kwargs else kwargs.get("clockwise")
        dx, dy = self.direction
        if clockwise:
            self.direction = (dy, -dx)
        else:
            self.direction = (-dy, dx)

    def move(self,**kwargs):
        """
        Move robot to the next position based on its direction.
        If the robot has a payload, move the payload as well.
        """
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.model.grid.move_agent(self, (self.x, self.y))

        #move payload
        for box in self.payload:
            box.x += self.direction[0]
            box.y += self.direction[1]
            self.model.grid.move_agent(box, (box.x, box.y))

    def pick_up(self,**kwargs):
        """
        Pick up the payload from the space ahead.
        """
        
        new_pos = (self.x+self.direction[0], self.y+self.direction[1])
        on_sight = [ obj for obj in self.model.grid.get_cell_list_contents([new_pos])[1:] if isinstance(obj,Box) and obj.state == UNDONE]

        
        if len(on_sight) > 0:
            self.payload = on_sight
            self.load_state = BUSY

            for box in self.payload:
                box.state = DONE
                box.x = self.x
                box.y = self.y
                self.model.grid.move_agent(box, (box.x,box.y))
            

    def drop_off(self,**kwargs):
        """
        Drop off the payload at the drop off point.
        """
        new_pos = (self.x+self.direction[0], self.y+self.direction[1])
        
        for box in self.payload:
                box.x = new_pos[0]
                box.y = new_pos[1]
                self.model.grid.move_agent(box, (box.x,box.y))

        self.load_state = FREE
        self.payload = []
        # turns facing opposite direction
        self.turn(clockwise=True)
        self.turn(clockwise=True)
      

    def read_mv(self):
        """
        Simulates a machine vision subsystem that detects what type of object is in the space ahead.
        Returns a string indicating the type of object, or 'UNKNOWN' if no object is found.
        """
        next_x = self.x + self.direction[0]
        next_y = self.y + self.direction[1]

        # Check if the next position is within bounds
        if not (0 <= next_x < NUMBER_OF_CELLS) or not (0 <= next_y < NUMBER_OF_CELLS):
            return WALL

        contents = self.model.grid.get_cell_list_contents([(next_x, next_y)])
        if not contents or (len(contents) == 1 and isinstance(contents[0], Tile)):
            return CLEAR
        else:
            for obj in contents:
                if isinstance(obj, Box):
                    return BOX
                elif isinstance(obj, Rack):
                    return RACK
                elif isinstance(obj, PickerRobot):
                    return ROBOT
        return UNKNOWN
        

class Box(mesa.Agent):
    """Represents a Box in the warehouse."""
    def __init__(self, id, pos, model):
        """
        Intialise state and position of the box
        """
        super().__init__(id, model)
        self.state = UNDONE
        self.x, self.y = pos

class Rack(mesa.Agent):
    """Represents a static Rack in the warehouse."""
    def __init__(self, id, pos, model):
        super().__init__(id, model)
        self.x, self.y = pos

class Tile(mesa.Agent):
    """Represents a static Tile in the warehouse."""
    def __init__(self, id, pos, model):
        super().__init__(id, model)
        self.x, self.y = pos
        self.is_target = False
    
    def step(self):
        """
        Tile's step function. It will make tile to become green if selected as target.
        """
        if (self.x,self.y) in self.model.targets.values():
            self.is_target = True
        else:
            self.is_target = False