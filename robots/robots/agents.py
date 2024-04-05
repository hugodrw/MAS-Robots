import mesa

from .random_walk import RandomWalker
from .shortsight_walk import ShortSightWalker


class Robot(ShortSightWalker):
    """
    Wooohooo robots!
    """

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)
        self.wastelist = []
        

    def step(self):
        """
        A model step. 
        """
        self.greedy_move()
        # self.random_move()

        if len(self.wastelist) > 0:
            print("I have waste!")
            print('items in the list: ', len(self.wastelist))


class Waste(mesa.Agent):
    """
    Waste baby!
    """

    def __init__(self, unique_id, pos, model):
        """

        Args:

        """
        super().__init__(unique_id, model)
        pass

    def step(self):
        pass