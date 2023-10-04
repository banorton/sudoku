class Positional_Element:
    def __init__(self, pos: tuple):
        self.pos = pos
        self.num = self.pos_to_num(pos)

    def pos_to_num(pos: tuple) -> int:
        return


class Cell(Positional_Element):
    def __init__(self, pos: tuple):
        self.val = 0
        self.notes = []
        super(self)


class Box(Positional_Element):
    def __init__(self, pos: tuple):
        self.cell_arr = self._generate_cell_arr()
        super(self)

    def _generate_cell_arr():
        return
