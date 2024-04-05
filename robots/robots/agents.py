import mesa

from .random_walk import RandomWalker
from .shortsight_walk import ShortSightWalker


class Robot(ShortSightWalker):
    """
    Robots!
    """

    def __init__(self, unique_id, pos, model, range, moore, colour='yellow'):
        super().__init__(unique_id, pos, model, range, moore=moore)
        self.wastelist = []
        self.colour = colour
        self.policy = 'greedy'
        
    
    def percept(self):
        # The robot is very intrsopective
        if len(self.wastelist) > 0:
            print("I have waste!")
            print('items in the list: ', len(self.wastelist))
    
    def deliberate(self):
        if len(self.wastelist) == 2:
            self.policy = 'go_to_dropoff_zone'
        else:
            self.policy = 'greedy'

    
    def do(self):
        if self.policy == 'greedy':
            self.greedy_move()
        elif self.policy == 'go_to_dropoff_zone':
            self.move_right()
            
    def step(self):
        """
        A model step. 
        """
        self.percept()
        self.deliberate()
        self.do()
        # self.random_move()




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