"""
Generalized behavior for random walking, one grid cell at a time.
"""

import mesa


class ShortSightWalker(mesa.Agent):
    """
    Class implementing short sight walker methods in a generalized manner.

    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    grid = None
    x = None
    y = None
    moore = True

    def __init__(self, unique_id, pos, model, moore=True):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def greedy_move(self):
        """
        If there is waste in the adjacent cells, move to the cell with the waste.
        """
        # Find the available cells
        # TODO: limit to the robot zone? ATM limit to grid
        available_cells = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        print('next_moves: ', available_cells)
        next_move = None
        for cell in available_cells:
            cell_contents = self.model.grid.get_cell_list_contents(cell)
            for content in cell_contents:
                    print('content name: ', content.__class__.__name__)  
                    if content.__class__.__name__ == 'Waste':
                        print('I found waste!')
                        next_move = cell
                        break
        if next_move is None:
            print('No waste found!')
            next_move = self.random.choice(available_cells)
        # Now move:
        self.model.grid.move_agent(self, next_move)
