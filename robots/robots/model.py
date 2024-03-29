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

from .agents import Waste
from .scheduler import RandomActivationByTypeFiltered


class RadioactiveEnv(mesa.Model):
    """
    Wolf-Sheep Predation Model
    """
    

    def __init__(
        self,
        width=20,
        height=20,
        initial_waste=5
    ):
        """
        Create a model with wastes to move.

        Args:

        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_waste = initial_waste
        
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
        for i in range(self.initial_waste):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            waste = Waste(self.next_id(), (x, y), self)
            self.grid.place_agent(waste, (x, y))
            self.schedule.add(waste)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        pass

    def run_model(self, step_count=200):
        pass
