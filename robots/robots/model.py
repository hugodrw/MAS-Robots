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

from .agents import Waste, Robot
from .scheduler import RandomActivationByTypeFiltered


class RadioactiveEnv(mesa.Model):
    """
    Radioactive environment model
    """
    

    def __init__(
        self,
        width=20,
        height=20,
        initial_wastes=25,
        initial_robots=5
    ):
        """
        Create a model with wastes to move.

        Args:

        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_wastes = initial_wastes
        self.initial_robots = initial_robots
        
        # Setup the scheduler
        self.schedule = RandomActivationByTypeFiltered(self)

        # Initiliase the map
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=False)

        # Setup the data collector
        self.datacollector = mesa.DataCollector(
            {
                "Waste": lambda m: m.schedule.get_type_count(Waste)
            }
        )

        # Add the wastes
        for i in range(self.initial_wastes):
            # TODO - check if the cell is already occupied
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            waste = Waste(self.next_id(), (x, y), self)
            self.grid.place_agent(waste, (x, y))
            self.schedule.add(waste)

        # Add the robots
        for i in range(self.initial_robots):
            # TODO - check if the cell is already occupied
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            robot = Robot(self.next_id(), (x, y), self, True)
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