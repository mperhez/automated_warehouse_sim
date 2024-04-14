from pydoc import doc
import mesa
import random
import numpy as np
from random import randint
from warehouse.agents import *
from .constants import *



class Warehouse(mesa.Model):
    """ Model representing an automated warehouse"""

    def __init__(self, n_robots, n_boxes, width=NUMBER_OF_CELLS, height=NUMBER_OF_CELLS):
        """
            Create a new warehouse model with the given parameters.
        """
        self.schedule = mesa.time.RandomActivationByType(self)
        self.n_robots = n_robots
        self.n_boxes = n_boxes
        self.n_racks = NUMBER_OF_RACKS
        self.targets = {}
        self.ticks = 0
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        
        ids = 0

        #Create tiles
        tiles_pos = [ (i,j) for i in range(width) for j in range(height)]
        for i,tile_pos in enumerate(tiles_pos):
            ids += 1
            tile =  Tile(ids,tile_pos,self)
            self.schedule.add(tile)
            self.grid.place_agent(tile,tile_pos)

        #Create Picker Robots
        for n in range(self.n_robots):
            ids += 1
            x = 1
            y = 1
            while True:
                y = self.random.randint(1,height-1)
                if len(self.grid.get_cell_list_contents((x,y)))==1:
                    break
        
            pr = PickerRobot(ids,(x,y),self)
            self.schedule.add(pr)            
            self.grid.place_agent(pr,(x,y))
            self.targets[ids] = None
            
        #Create boxes
        for n in range(self.n_boxes):
            ids += 1
            while True:
                x = randint(1,width-1)
                y = randint(1,height-1)
                if len(self.grid.get_cell_list_contents((x,y)))==1:
                    break

            b = Box(ids,(x,y),self)
            self.schedule.add(b)            
            self.grid.place_agent(b,(x,y))
        
        #Create racks
        for n in range(self.n_racks):
            ids += 1
            while True:
                
                x = random.choice(range(0,width-1))
                y = random.choice(range(0,height-1))
                
                if len(self.grid.get_cell_list_contents((x,y)))==1:
                    break
            
            r = Rack(ids,(x,y),self)
            
            self.schedule.add(r)            
            self.grid.place_agent(r,(x,y))

        self.running = True

    def step(self):
        """
        * Run while there are Undone boxes, otherwise stop running model.
        """
        self.ticks += 1
        boxes = [a for a in self.schedule.agents if isinstance(a,Box) if a.state == UNDONE or a.pos != DROP_OFF_POINT]
        
        if len(boxes) > 0:
            self.schedule.step()
        else:
           self.running = False
