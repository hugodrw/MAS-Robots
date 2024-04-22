import mesa

from .agents import Waste, Robot, Grid_Tile
from .scheduler import RandomActivationByTypeFiltered
from .percepts import Percept
from robots.communication.agent.CommunicatingAgent import CommunicatingAgent
from robots.communication.message.Message import Message
from robots.communication.message.MessagePerformative import MessagePerformative
from robots.communication.message.MessageService import MessageService


class RadioactiveEnv(mesa.Model):
    """
        Base Class for the Radioactive Environment
    """
    def __init__(
        self,
        width=21,
        height=5,
        initial_wastes_per_zone=6,
        initial_robots_per_zone=1
        # TODO: Hardcoded for now in server
    ):
        """
        Create a model with wastes to move.

        Args:

        """
        super().__init__()
         # set messages 
        self.schedule = RandomActivationByTypeFiltered(self)
        self.__messages_service = MessageService(self.schedule)
        MessageService.get_instance().set_instant_delivery(False)
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
                # x = 0
                y = self.random.randrange(self.height)
                robot = Robot(self.next_id(), (x, y), self,zone_value, True,colour=zone_key)
                self.grid.place_agent(robot, (x, y))
                self.schedule.add(robot)

        
    def do(self, agent, action):
        '''
            Take the action determined and return an observation
        '''
        #  =====  Do the action  =========
        # Check if the action is a movement
        movement, handlewaste = action
        pickedup_waste = False
        if movement != None:
            self.grid.move_agent(agent, movement)
        if handlewaste != None:
            # Do the waste handling
            if handlewaste == 'PickUp':
                pickedup_waste =True
                self.collect_waste(agent)
            elif handlewaste == 'Transform':
                self.transform_waste(agent)
            elif handlewaste == 'DropOff': # only for red robot
                self.drop_waste(agent)
            elif handlewaste == 'DropOffandSendMessage':
                self.drop_waste(agent)
                # Send a message to the other robots to let them know that the waste has been dropped off
                self.inform_waste_location(agent)
               

        #  ====== Get the info needed for percept  =======
        # Neighbour tuple list
        current_pos = agent.pos
        neighbours = []
        # All neighbours in grid
        all_neighbours = list(self.grid.get_neighborhood(current_pos, True, True)) #check moore
        # Restric to the robot's zone
        # Restrict the robot to it's zones
        restricted_neighbours = []
        for cell in all_neighbours:
            if cell[0] in range(0,agent.x_range[1]):
                restricted_neighbours.append(cell)

        # Look at contents of the restrcited neighbours
        for cell in restricted_neighbours:
            cell_contents = self.grid.get_cell_list_contents(cell)
            neighbours.append((cell, cell_contents))

        # Get the waste list so it can be added to the percepts
        waste_list = agent.waste_list
        # Get the waste location send to store after
        waste_location = None
        # check messages 
        new_messages = agent.get_new_messages()
        if len(new_messages) != 0:
            print("y a des messages")
            for message in new_messages:
                if message.get_performative() == MessagePerformative.INFORM_REF:
                    waste_location = message.get_content()
                    print('Waste location received from message: ', waste_location)
                
        # Build percept object to be sent to agent
        percept = Percept(neighbours, current_pos, waste_list,waste_location,pickedup_waste)

        return percept

    def collect_waste(self, agent):
        '''
            Add the waste to the robot's waste list if it is on the same cell
            Return the current waste list
        '''
        # Add waste to the agent's list if it is on the same cell
        if isinstance(agent, Robot):            
            cellmates = self.grid.get_cell_list_contents([agent.pos])
            for cellmate in cellmates:
                if isinstance(cellmate, Waste) and agent.colour == cellmate.colour:
                    agent.waste_list.append(cellmate)
                    self.grid.remove_agent(cellmate)
                    self.schedule.remove(cellmate)
        
    
    def transform_waste(self, agent):
        '''
            Deletes one waste from the list
            Changes the color of the remaining waste
            If green, transform to yellow
            If yellow, transform to red
        '''
        print('Transforming waste')
        print('Current waste list: ', agent.waste_list)

        agent.waste_list.pop(0)
        if agent.waste_list[0].colour == 'green':
            agent.waste_list[0].colour = 'yellow'
        elif agent.waste_list[0].colour == 'yellow':
            agent.waste_list[0].colour = 'red'

        print('New waste list: ', agent.waste_list)

    def drop_waste(self, agent):
        '''
            Add the current waste to the grid at the current location, and delete it from the wastelist
        '''
        waste = agent.waste_list.pop(0)
        self.grid.place_agent(waste, agent.pos)
        self.schedule.add(waste)
        
    def inform_waste_location(self, agent):
        '''
            green robot sends a message to the yellow robot
            yellow robot sends a message to the red robot
        '''
        if agent.colour == 'yellow' :
            # send a message to the red robot
            for target_agent in self.schedule.agents:
                if isinstance(target_agent, Robot) and target_agent.colour == 'red':
                    message = Message(agent.colour ,target_agent.colour, MessagePerformative.INFORM_REF, agent.pos)
                    agent.send_message(message) # message send to red 
                    print('Message sent from yellow to red robot')
                
        if agent.colour == 'green':
            for target_agent in self.schedule.agents:
                if isinstance(target_agent, Robot) and target_agent.colour == 'yellow':
                    message = Message(agent.colour,target_agent.colour , MessagePerformative.INFORM_REF, agent.pos)
                    agent.send_message(message) # message send to red 
                    print('Message sent from green to yellow robot')

            
        
    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self, step_count=200):
        pass
