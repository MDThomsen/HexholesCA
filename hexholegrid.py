import cellstates as states

class Hexholegrid:
    gridSize = 1000

    def __init__(self):
        self.grid = [[states.Cell(i,j,self.grid) for i in range(self.gridSize)] for j in range(self.gridSize)]

    def performIterations(self,iterations):
        if iterations == 0:
            return
        if iterations > 0:
            self.performIteration()
            self.performIterations(iterations-1)

    def performIteration(self):
        newgrid = self.grid

        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                newgrid[i][j] = self.grid[i][j].coordinate(self.grid)

        self.grid = newgrid