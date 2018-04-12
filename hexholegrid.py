import cellstates as states
from PIL import Image,ImageDraw
import os
import datetime

class HexholeGrid:

    def __init__(self,queue,p1,p2,p3,full_p,only_p,gridSize):
        self.queue = queue
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.full_p = full_p
        self.only_p = only_p
        self.gridSize = gridSize

        self.grid = [[states.FullCell(i,j,p1,p2,p3,full_p,only_p) for i in range(self.gridSize)] for j in range(self.gridSize)]
        for k in range(self.gridSize):
            for l in range(self.gridSize):
                self.grid[k][l].initialize_neighbours(self.grid)

    def perform_iterations(self, iterations):
        if iterations == 0:
            self.draw_and_save_result()
            return
        if iterations > 0:
            print("Iterations left: " + str(iterations))
            self.perform_iteration()
            if(self.queue is not None):
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

    #Draws the result and saves in a file in the same directory as the application.
    def draw_and_save_result(self):
        cols = len(self.grid)
        rows = len(self.grid)
        cell_side_length = 10

        im = Image.new("RGB", ((cell_side_length+5) * cols,cell_side_length * rows))
        draw = ImageDraw.Draw(im)

        rowNumber = 0
        for row in range(rows):
            columnNumber = 0
            rowNumber = rowNumber + 1
            for col in range(cols):
                columnNumber = columnNumber + 1

                if(type(self.grid[row][col]) is states.FullCell):
                    fill = "green"
                elif(type(self.grid[row][col]) is states.OnlyACell):
                    fill = "orange"
                elif (type(self.grid[row][col]) is states.OnlyBCell):
                    fill = "yellow"
                else:
                    fill = "red"

                translation = rows*5-row*5
                draw.polygon([col * cell_side_length + 5 + translation,
                              row * cell_side_length,
                              col * cell_side_length + translation,
                              (row + 1) * cell_side_length,
                              (col + 1) * cell_side_length + translation,
                              (row + 1) * cell_side_length,
                              (col + 1) * cell_side_length +5 +translation,
                              row * cell_side_length],fill,"black")

        path = os.path.dirname(os.path.realpath(__file__))+"/"
        filename = "p1_"+str(self.p1)+"_p2_"+str(self.p2)+"_p3_"+str(self.p3)+"_FullToAB_"+str(self.full_p)+"_ABtoEmpty_"+str(self.only_p)
        timestamp = "_" + str(datetime.datetime.now())
        extension = ".png"
        fullname = path+filename+timestamp+extension

        im.save(fullname)
