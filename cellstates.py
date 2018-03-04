from abc import abstractmethod

class MetaCellClass:
    @classmethod
    def __subclasshook__(cls, subclass):
        required_attrs = getattr(cls, '_required_attrs', [])
        for attr in required_attrs:
            if any(attr in sub.__dict__ for sub in subclass.__mro__):
                continue
            return False
        return True

class Cell(metaclass=MetaCellClass):
    x = 0
    y = 0

    _required_attrs = ['determineTransformation']

    @abstractmethod
    def doIteration(self, grid):
        while False:
            yield None

    def __init__(self,x,y,grid,p1,p2,p3):
        self.x = x
        self.y = y
        self.grid = grid
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        northCoordinate = IndexUtility.north(x, y)
        eastCoordinate = IndexUtility.east(x, y)
        westCoordinate = IndexUtility.west(x, y)
        southCoordinate = IndexUtility.south(x, y)
        self.northCell = self.grid[northCoordinate[1]][northCoordinate[0]]
        self.eastCell = self.grid[eastCoordinate[1]][eastCoordinate[0]]
        self.westCell = self.grid[westCoordinate[1]][westCoordinate[0]]
        self.southCell = self.grid[southCoordinate[1]][southCoordinate[0]]

class FullCell(Cell):

    def doIteration(self, grid):
        pass

    def _isF1Valid(self):
        return (((isinstance(self.northCell,OnlyBCell) and isinstance(self.eastCell,OnlyBCell)) or (isinstance(self.northCell,EmptyCell) and isinstance(self.eastCell,EmptyCell))) \
               and ((isinstance(self.southCell,OnlyACell) and isinstance(self.westCell,OnlyACell)) or (isinstance(self.southCell,EmptyCell) and isinstance(self.westCell,EmptyCell))))

    def _isF21Valid(self,p3):
        #IF ONE OF WHAT?

    def _isF22Valid(self,p3):
        pass

    def _isF31Valid(self,p2):
        pass

    def _isF32Valid(self,p2):
        pass

    def _isF33Valid(self,p2):
        pass


    def _isF41Valid(self,p1):
        pass

    def _isF42Valid(self,p1):
        pass

class OnlyACell(Cell):
    def doIteration(self, grid):
        pass

    def _isA1Valid(self):
        pass

    def _isA2Valid(self):
        pass

    def _isA3Valid(self):
        pass


class OnlyBCell(Cell):
    def doIteration(self, grid):
        pass

    def _isB1Valid(self):
        pass

    def _isB2Valid(self):
        pass

    def _isB3Valid(self):
        pass

class EmptyCell(Cell):
    def doIteration(self, grid):
        pass

class IndexUtility:
    def __init__(self,grid):
        self.grid = grid

    def north(self,x,y):
        return self._calculateCoordinate(x, y, 0, 1)

    def south(self,x,y):
        return self._calculateCoordinate(x, y, 0, -1)

    def west(self,x,y):
        return self._calculateCoordinate(x, y, -1, 0)

    def east(self,x,y):
        return self._calculateCoordinate(x, y, 1, 0)

    def _calculateCoordinate(self,x,y,xDir,yDir):
        newX = (x + xDir) % len(self.grid)
        newY = (y + yDir) % len(self.grid)
        return (newX,newY)