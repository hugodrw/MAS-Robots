"""
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

import mesa

from .agents import Waste, Robot, Grid_Tile
from .scheduler import RandomActivationByTypeFiltered


class RadioactiveEnv(mesa.Model):
    """
    Radioactive environment model
    """
    

    def __init__(
        self,
        width=21,
        height=5,
        initial_wastes_per_zone=2,
        initial_robots_per_zone=1
        # TODO: Hardcoded for now in server
    ):
        """
        Create a model with wastes to move.

        Args:

        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_wastes_per_zone = initial_wastes_per_zone
        self.initial_robots_per_zone = initial_robots_per_zone

        # Check if the width is divisible by 3, otherwise throw an error
        if self.width % 3 != 0:
            raise ValueError("The grid width must be divisible by 3")
        
        # Setup the zone locations
        self.zone_locations = {'green':(0, self.width//3),
            'yellow':(self.width//3, self.width*2//3),
            'red':(self.width*2//3, self.width)}

        # Setup the scheduler
        self.schedule = RandomActivationByTypeFiltered(self)

        # Setup the data collector
        self.datacollector = mesa.DataCollector(
            {
                "Waste": lambda m: m.schedule.get_type_count(Waste)
            }
        )
        
        # Initiliase the map
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=False)

        # Place wastes, robots and tiles on the grid
        for zone_key, zone_value in self.zone_locations.items():

            # Fill each zone with tiles of its colour 
            for x in range(zone_value[0], zone_value[1]):
                for y in range(self.height):
                    tile = Grid_Tile(self.next_id(), (x, y), self, colour=zone_key)
                    self.grid.place_agent(tile, (x, y))
                    self.schedule.add(tile)

            # Add the wastes to the zone
            for i in range(self.initial_wastes_per_zone):
                # TODO - check if the cell is already occupied
                # Limit the x range to the width
                x = self.random.randrange(zone_value[0], zone_value[1])
                y = self.random.randrange(self.height)
                waste = Waste(self.next_id(), (x, y), self, colour=zone_key)
                self.grid.place_agent(waste, (x, y))
                self.schedule.add(waste)
            
            # Add the robot to the zone
            for i in range(self.initial_robots_per_zone):
                # TODO - check if the cell is already occupied
                x = self.random.randrange(zone_value[0], zone_value[1])
                y = self.random.randrange(self.height)
                robot = Robot(self.next_id(), (x, y), self,zone_value, True,colour=zone_key)
                self.grid.place_agent(robot, (x, y))
                self.schedule.add(robot)

    def collect_waste(self):
        '''
            Add the waste to each robot's waste list if it is on the same cell
        '''
        for agent in self.schedule.agents:
            if isinstance(agent, Robot):            
                cellmates = self.grid.get_cell_list_contents([agent.pos])
                for cellmate in cellmates:
                    if isinstance(cellmate, Waste):
                        agent.wastelist.append(cellmate)
                        self.grid.remove_agent(cellmate)
                        self.schedule.remove(cellmate)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        self.collect_waste()

    def run_model(self, step_count=200):
        pass
