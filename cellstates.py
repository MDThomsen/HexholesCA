from abc import abstractmethod
import random

class Cell:

    @abstractmethod
    def do_iteration(self):
        while False:
            yield None

    def __init__(self, x, y, p1, p2, p3, full_p, only_p):
        self.x = x
        self.y = y
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.full_p = full_p
        self.only_p = only_p

    def initialize_neighbours(self, grid):
        index_utility = IndexUtility()
        north_coordinate = index_utility.north(grid, self.x, self.y)
        east_coordinate = index_utility.east(grid, self.x, self.y)
        west_coordinate = index_utility.west(grid, self.x, self.y)
        south_coordinate = index_utility.south(grid, self.x, self.y)
        self.northCell = grid[north_coordinate[1]][north_coordinate[0]]
        self.eastCell = grid[east_coordinate[1]][east_coordinate[0]]
        self.westCell = grid[west_coordinate[1]][west_coordinate[0]]
        self.southCell = grid[south_coordinate[1]][south_coordinate[0]]

    def north_is(self, celltype):
        return type(self.northCell) is celltype

    def south_is(self, celltype):
        return type(self.southCell) is celltype

    def west_is(self, celltype):
        return type(self.westCell) is celltype

    def east_is(self, celltype):
        return type(self.eastCell) is celltype


class FullCell(Cell):
    def do_iteration(self):
        if self._is_f1_valid():
            return EmptyCell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)

        elif self._is_f21_valid():
            return OnlyBCell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)

        elif self._is_f22_valid():
            return OnlyACell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)

        elif self._is_f31_valid():
            return OnlyACell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)

        elif self._is_f32_valid():
            return OnlyACell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)

        elif self._is_f33_valid():
            if random.random() < 0.5:
                return OnlyACell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)
            else:
                return OnlyBCell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)

        elif self._is_f41_valid():
            return OnlyACell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)

        elif self._is_f42_valid():
            return OnlyBCell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)

        elif self._should_transform():
            if random.random() < 0.5:
                return OnlyACell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)
            else:
                return OnlyBCell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)

        else:
            return self

    # transform to onlyA or onlyB cell
    def _should_transform(self):
        return random.random() < self.full_p

    # Co-ordination -4:
    def _is_f1_valid(self):
        return (
            ((self.north_is(OnlyBCell) or self.north_is(EmptyCell)) and
             (self.east_is(OnlyBCell) or self.east_is(EmptyCell)))
            and ((self.south_is(OnlyACell) or self.south_is(EmptyCell)) and (
                self.west_is(OnlyACell) or self.west_is(EmptyCell))))

    # Co-ordination -3:
    def _is_f21_valid(self):
        if (not ((self.north_is(OnlyBCell) or self.north_is(EmptyCell)) is
                     (self.east_is(OnlyBCell) or self.east_is(EmptyCell)))
            and ((self.south_is(OnlyACell) or self.south_is(EmptyCell)) and (
                        self.west_is(OnlyACell) or self.west_is(EmptyCell)))):
            return random.random() < self.p3

    def _is_f22_valid(self):
        if (not ((self.south_is(OnlyACell) or self.south_is(EmptyCell)) is (
                    self.west_is(OnlyACell) or self.west_is(EmptyCell)))
            and ((self.north_is(OnlyBCell) or self.north_is(EmptyCell)) and (
                        self.east_is(OnlyBCell) or self.east_is(EmptyCell)))):
            return random.random() < self.p3

    # Co-ordination -2:
    def _is_f31_valid(self):
        if (((self.north_is(OnlyBCell) and self.east_is(OnlyBCell)) or (
                    self.north_is(EmptyCell) and self.east_is(EmptyCell)))
            and (self.south_is(FullCell) or self.south_is(OnlyBCell)) and (
                    self.west_is(FullCell) or self.west_is(OnlyBCell))):
            return random.random() < self.p2

    def _is_f32_valid(self):
        if (((self.south_is(OnlyBCell) and self.west_is(OnlyBCell)) or (
                    self.south_is(EmptyCell) and self.west_is(EmptyCell)))
            and (self.north_is(FullCell) or self.north_is(OnlyBCell)) and (
                    self.east_is(FullCell) or self.east_is(OnlyBCell))):
            return random.random() < self.p2

    def _is_f33_valid(self):
        if (not ((self.north_is(OnlyACell) or self.north_is(EmptyCell)) is (
                    self.east_is(OnlyACell) or self.east_is(EmptyCell)))
            and not ((self.south_is(OnlyBCell) or self.south_is(EmptyCell)) is (
                        self.west_is(OnlyBCell) or self.west_is(EmptyCell)))):
            return random.random() < self.p2

    # Co-ordination -1:
    def _is_f41_valid(self):
        if (not ((self.north_is(OnlyBCell) or self.north_is(EmptyCell)) is (
                    self.east_is(OnlyBCell) or self.east_is(EmptyCell)))
            and (self.south_is(FullCell) or self.south_is(OnlyBCell)) and (
                    self.west_is(FullCell) or self.west_is(OnlyBCell))):
            return random.random() < self.p1

    def _is_f42_valid(self):
        if (not ((self.south_is(OnlyACell) or self.south_is(EmptyCell)) is (
                    self.west_is(OnlyACell) or self.west_is(EmptyCell)))
            and (self.north_is(FullCell) and self.east_is(FullCell))):
            return random.random() < self.p1


class OnlyACell(Cell):
    def do_iteration(self):
        if self._is_a1_valid():
            return EmptyCell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)
        elif self._is_a2_valid():
            return EmptyCell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)
        elif self._is_a3_valid():
            return EmptyCell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)
        elif self._should_transform():
            return EmptyCell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)
        else:
            return self

    def _should_transform(self):
        return random.random() < self.only_p

    def _is_a1_valid(self):
        return (self.south_is(OnlyACell) and self.west_is(OnlyACell)) or (
            self.south_is(EmptyCell) and self.west_is(EmptyCell))

    def _is_a2_valid(self):
        if (not ((self.south_is(OnlyACell) or self.south_is(EmptyCell)) is (
                    self.west_is(OnlyACell) or self.west_is(EmptyCell)))):
            return random.random() < self.p3

    def _is_a3_valid(self):
        if ((self.south_is(FullCell) and self.west_is(FullCell)) or (
                    self.south_is(OnlyBCell) and self.west_is(OnlyBCell))):
            return random.random() < self.p2


class OnlyBCell(Cell):
    def do_iteration(self):
        if self._is_b1_valid():
            return EmptyCell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)
        elif self._is_b2_valid():
            return EmptyCell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)
        elif self._is_b3_valid():
            return EmptyCell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)
        elif self._should_transform():
            return EmptyCell(self.x, self.y, self.p1, self.p2, self.p3, self.full_p, self.only_p)
        else:
            return self

    def _should_transform(self):
        return random.random() < self.only_p

    def _is_b1_valid(self):
        return (self.north_is(OnlyBCell) and self.east_is(OnlyBCell)) or (
            self.north_is(EmptyCell) and self.east_is(EmptyCell))

    def _is_b2_valid(self):
        if (not ((self.north_is(OnlyBCell) or self.north_is(EmptyCell)) is (
                    self.east_is(OnlyBCell) or self.east_is(EmptyCell)))):
            return random.random() < self.p3

    def _is_b3_valid(self):
        if ((self.north_is(FullCell) and self.east_is(FullCell)) or (
                    self.north_is(OnlyACell) and self.east_is(OnlyACell))):
            return random.random() < self.p2

class EmptyCell(Cell):
    def do_iteration(self):
        return self

class IndexUtility:

    def north(self, grid, x, y):
        return self._calculate_indices(grid, x, y, 0, -1)

    def south(self, grid, x, y):
        return self._calculate_indices(grid, x, y, 0, 1)

    def west(self, grid, x, y):
        return self._calculate_indices(grid, x, y, -1, 0)

    def east(self, grid, x, y):
        return self._calculate_indices(grid, x, y, 1, 0)

    @staticmethod
    def _calculate_indices(grid, x, y, x_dir, y_dir):
        new_x = (x + x_dir) % len(grid)
        new_y = (y + y_dir) % len(grid)
        return [new_x, new_y]