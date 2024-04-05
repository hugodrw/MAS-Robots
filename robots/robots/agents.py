import mesa

from .random_walk import RandomWalker
from .shortsight_walk import ShortSightWalker


class Robot(ShortSightWalker):
    """
    Wooohooo robots!
    """

    def __init__(self, unique_id, pos, model, moore, colour='yellow'):
        super().__init__(unique_id, pos, model, moore=moore)
        self.wastelist = []
        self.colour = colour
        

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

    def __init__(self, unique_id, pos, model, colour='yellow'):
        super().__init__(unique_id, model)
        self.colour = colour
        pass

    def step(self):
        pass

class Grid_Tile(mesa.Agent):
    """
    Colour baby!
    """

    def __init__(self, unique_id, pos, model, colour='yellow'):
        super().__init__(unique_id, model)
        self.colour = colour
        pass

    def step(self):
        pass