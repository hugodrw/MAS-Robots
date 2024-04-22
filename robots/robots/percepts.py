

class Percept():
    def __init__(self, neighbours, current_pos, waste_list):
        self.neighbours = neighbours # List of tuples (cell_location, cell_contents)
        self.current_pos = current_pos # Equiv of base_cells
        self.waste_list = waste_list


        # TODO: waste position


