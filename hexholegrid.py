import cellstates as states

class Hexholegrid:
    gridSize = 1000

    def __init__(self,queue,p1,p2,p3,full_p,only_p):
        self.queue = queue
        self.grid = [[states.FullCell(i,j,p1,p2,p3,full_p,only_p) for i in range(self.gridSize)] for j in range(self.gridSize)]
        for k in range(self.gridSize):
            for l in range(self.gridSize):
                self.grid[k][l].initialize_neighbours(self.grid)

    def perform_iterations(self, iterations):
        if iterations == 0:
            return
        if iterations > 0:
            self.perform_iteration()
            self.queue.put(("iteration",iterations-1))
            self.perform_iterations(iterations - 1)

    def perform_iteration(self):
        self.newgrid = self.grid

        for i in range(self.gridSize):
            for j in range(self.gridSize):
                self.newgrid[i][j] = self.grid[i][j].do_iteration()

        for i in range(self.gridSize):
            for j in range(self.gridSize):
                self.newgrid[i][j].initialize_neighbours(self.newgrid)

        self.grid = self.newgrid
        self.newgrid = None
