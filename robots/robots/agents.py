import mesa

from .random_walk import RandomWalker


class Robot(RandomWalker):
    """
    Wooohooo robots!
    """

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)
        

    def step(self):
        """
        A model step. 
        """
        self.random_move()


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