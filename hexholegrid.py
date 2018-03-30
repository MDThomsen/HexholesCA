import cellstates as states

class Hexholegrid:
    gridSize = 1000

    def __init__(self,queue,p1,p2,p3,full_p,only_p):
        self.queue = queue
        self.grid = [[states.FullCell(i,j,p1,p2,p3,full_p,only_p) for i in range(self.gridSize)] for j in range(self.gridSize)]
        for k in range(self.gridSize):
            for l in range(self.gridSize):
                self.grid[k][l].initialize_neighbours(self.grid)

    def performIterations(self,iterations):
        if iterations == 0:
            return
        if iterations > 0:
            self.performIteration()
            self.queue.put(("iteration",iterations-1))
            self.performIterations(iterations-1)

    def performIteration(self):
        newgrid = self.grid

        for i in range(self.gridSize):
            for j in range(self.gridSize):
                newgrid[i][j] = self.grid[i][j].do_iteration()

        for i in range(self.gridSize):
            for j in range(self.gridSize):
                newgrid[i][j].initialize_neighbours(newgrid)

        self.grid = newgrid

