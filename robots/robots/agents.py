import mesa
from collections import namedtuple

from .random_walk import RandomWalker
from .shortsight_walk import ShortSightWalker
import random


# Helper classes
class KnowledgeBase():
    # The knowledge base for the robot
    def __init__(self, colour, x_range):
        self.colour = colour
        self.x_range = x_range

        # Taken from percepts
        self.neighbours = None
        self.current_pos = None
        self.waste_list = []

# Helper Functions
def update(knowledge, percepts):
    # Add info to the knowledge base
    knowledge.neighbours = percepts.neighbours
    knowledge.current_pos = percepts.current_pos
    knowledge.waste_list = percepts.waste_list
    
    return knowledge

def move_right(knowledge: KnowledgeBase):
    """
    Move right, except if already at the end of the zone
    Return: next_move (x,y)
    """
    # Check if the robot is at the right edge of the zone
    if knowledge.current_pos[0] == knowledge.x_range[1]-1:
        print('Cannot go right, I am already at the right edge of my zone!!')
        return

    right_move = (knowledge.current_pos[0]+1, knowledge.current_pos[1])
    
    return right_move

def look_for_waste(knowledge: KnowledgeBase):
    '''
        Look in the robot's neighbourhood and move to the waste if found
        Otherwise move randomly
        Return: next_move (x,y)
    '''
    next_move = None
    for neighbour in knowledge.neighbours:
        # Neighbour is a tuple (cell_location, cell_contents)
        cell_location, cell_contents = neighbour
        for content in cell_contents:
                if content.__class__.__name__ == 'Waste' and content.colour == knowledge.colour:
                    print('I found waste!')
                    next_move = cell_location
                    break
    if next_move is None:
        print('No waste found!')
        next_move = random.choice(knowledge.neighbours)[0]
    
    return next_move


def deliberate(knowledge: KnowledgeBase):
    '''
        Takes info from the knowledge
        Returns an action for the environment
        Returns:
        Movement: (x,y)
        HandleWaste: 'PickUp', 'DropOff', 'Transform'
    '''

    movement = None
    handlewaste = None

    if len(knowledge.waste_list) == 2:
        movement = move_right(knowledge)

    else:
        # Greedy move
        movement = look_for_waste(knowledge)

    return movement, handlewaste


class Robot(ShortSightWalker):
    """
    Robots!
    """

    def __init__(self, unique_id, pos, model, x_range, moore, colour='yellow'):
        super().__init__(unique_id, pos, model, x_range, colour, moore=moore)
        # self.wastelist = []
        # self.policy = 'greedy'

        # Setup the knowledge base
        self.knowledge = KnowledgeBase(colour, x_range)
        self.waste_list = []
        self.percepts = None
    
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
        # self.percept()
        # self.deliberate()
        # self.do()
        # # self.random_move()
        if self.percepts is not None:
            # Normal case
            print('normal')
            self.knowledge = update(self.knowledge, self.percepts)
            action = deliberate(self.knowledge) 
        else:
            # First observation
            action = (None, None)
            self.first_observation = False

        self.percepts = self.model.do(self,action)
        print('percepts: ', self.percepts)




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