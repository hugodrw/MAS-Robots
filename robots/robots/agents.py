import mesa
from collections import namedtuple
import random


from robots.communication.agent.CommunicatingAgent import CommunicatingAgent

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
        self.received_waste_locations= []

# Helper Functions
def update(knowledge, percepts):
    # Add info to the knowledge base
    knowledge.neighbours = percepts.neighbours
    knowledge.current_pos = percepts.current_pos
    knowledge.waste_list = percepts.waste_list
    if percepts.received_waste_location is not None:
        knowledge.received_waste_locations.append(percepts.received_waste_location)
    if percepts.pickedup_waste == True:
        # remove the current pos from the received waste locations
        if percepts.current_pos in knowledge.received_waste_locations:
            knowledge.received_waste_locations.remove(percepts.current_pos)
    
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
                if content.__class__.__name__ == 'Waste' and content.colour == knowledge.colour and cell_location[0] != knowledge.x_range[1]-1:
                    print('I found waste!')
                    next_move = cell_location
                    break
    if next_move is None:
        if len(knowledge.received_waste_locations) > 0:
            # there is at least one waste to go to
            target_location = knowledge.received_waste_locations[0]
            next_move = go_to_target_location(target_location, knowledge.current_pos)
        else : 
            print('No waste found!')
            next_move = random.choice(knowledge.neighbours)[0]
    
    return next_move


def go_to_target_location(target_location,current_location):

    current_x, current_y = current_location
    target_x, target_y = target_location

    # Calculate the differences in x and y coordinates
    dx = target_x - current_x
    dy = target_y - current_y
    
    # Determine the direction to move in each axis
    next_x = current_x + (dx // abs(dx) if dx != 0 else 0)
    next_y = current_y + (dy // abs(dy) if dy != 0 else 0)
    
    return (next_x, next_y)

def waste_available(knowledge: KnowledgeBase):
    '''
        Check if there is a waste at the current position
        Return boolean
    '''
    waste_here = False
    for neighbour in knowledge.neighbours:
        cell_location, cell_contents = neighbour
        for content in cell_contents:
                if content.__class__.__name__ == 'Waste' and content.colour == knowledge.colour and cell_location == knowledge.current_pos:
                    print('Waste available here!')
                    waste_here = True
                    break
    return waste_here


def deliberate(knowledge: KnowledgeBase):
    '''
        Takes info from the knowledge
        Returns an action for the environment
        Returns:
        Movement: (x,y)
        HandleWaste: 'PickUp', 'DropOffandSendMessage', 'Transform','DropOff'
        Note: Cannot do Movement and HandleWaste at same time for now
    '''

    movement = None
    handlewaste = None

    #  =======  Overall logic =======

    # Red robot logic, no transformation
    if knowledge.colour == 'red':
        # If it has a waste, move to the dropoff zone
        if len(knowledge.waste_list) == 1:
            if knowledge.current_pos[0] != knowledge.x_range[1]-1:
                movement = move_right(knowledge)
            else:
                handlewaste = 'DropOff'

        # If waste is available and it isn't in the dropoff zone, pick it up
        elif waste_available(knowledge) and knowledge.current_pos[0] != knowledge.x_range[1]-1:
            handlewaste = 'PickUp'
        # If waste is not available, move to the waste
        else:
            print('Red robot looking for waste')
            movement = look_for_waste(knowledge)
    # Other robots, with transformation
    else:
        # If it has two wastes, transform
        if len(knowledge.waste_list) == 2:
            handlewaste = 'Transform'
        # If it has one waste
        if len(knowledge.waste_list) == 1:
            # Check if the waste has been transformed
            if knowledge.waste_list[0].colour != knowledge.colour:
                # Move to the dropoff zone and drop
                if knowledge.current_pos[0] != knowledge.x_range[1]-1:
                    movement = move_right(knowledge)
                else:
                    handlewaste = 'DropOffandSendMessage'
            # If it is the robot's colour, look for more waste
            else:
                # If waste is available, pick it up
                if waste_available(knowledge):
                    handlewaste = 'PickUp'
                else:
                    # Look for more wastes
                    movement = look_for_waste(knowledge)
        # If no waste, look for waste
        else:
            # If waste is available, pick it up
            if waste_available(knowledge):
                handlewaste = 'PickUp'
            else:
                # Look for more wastes
                movement = look_for_waste(knowledge)



        


    # # Check if on the same cell as waste and capicity for more waste
    # if len(knowledge.waste_list) < 2:
    #     if waste_available(knowledge):
    #         # If waste is available, pick it up
    #         handlewaste = 'PickUp'
    #     else:
    #         # Normal movement if no waste available
    #         movement = look_for_waste(knowledge)
    

    # # Transform waste if 2 items in waste list and it is not red
    # if len(knowledge.waste_list) == 2 and knowledge.waste_list[0].colour != 'red':
    #     handlewaste = 'Transform'
    
    # # If waste is not the robot's colour or the waste is red
    # if len(knowledge.waste_list) == 1 and (knowledge.waste_list[0].colour == 'red' or knowledge.waste_list[0].colour != knowledge.colour):
    #     # If not in the dropoff zone, move to the dropoff zone
    #     if knowledge.current_pos[0] != knowledge.x_range[1]-1:
    #         movement = move_right(knowledge)
    #     # If in the dropoff zone, dropoff the waste
    #     else:
    #         handlewaste = 'DropOff'

    return movement, handlewaste


class Robot(CommunicatingAgent):
    """
    Robots!
    """

    def __init__(self, unique_id, pos, model, x_range, moore, colour='yellow'):
        # super().__init__(unique_id, pos, model, x_range, colour, moore=moore)
        # self.wastelist = []
        # self.policy = 'greedy'

        super().__init__(unique_id, model,colour)
        # Setup the knowledge base
        self.knowledge = KnowledgeBase(colour, x_range)
        # Generally available variables
        self.waste_list = []
        self.percepts = None
        self.x_range = x_range
        self.pos = pos
        self.colour = colour
    
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




class Waste(CommunicatingAgent):
    """
    Waste baby!
    """

    def __init__(self, unique_id, pos, model, colour='yellow'):
        super().__init__(unique_id, model,'waste')
        self.colour = colour
        pass

    def step(self):
        pass

class Grid_Tile(CommunicatingAgent):
    """
    Colour baby!
    """

    def __init__(self, unique_id, pos, model, colour='yellow'):
        super().__init__(unique_id, model,'tile')
        self.colour = colour
        
        pass

    def step(self):
        pass