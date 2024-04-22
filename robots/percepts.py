

class Percept():
    def __init__(self, neighbours, current_pos, waste_list,received_waste_location,pickedup_waste):
        self.neighbours = neighbours # List of tuples (cell_location, cell_contents)
        self.current_pos = current_pos # Equiv of base_cells
        self.waste_list = waste_list
        self.received_waste_location = received_waste_location  
        self.pickedup_waste = pickedup_waste 
        # TODO: waste position


