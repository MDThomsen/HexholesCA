import hexholegrid
import tkinter as tk
import os
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageDraw
import asyncio
import threading
import queue

import cellstates

class ResultFrame(tk.Frame):
    def __init__(self,parent,grid):
        self.parent = parent
        self.screen_width = self.parent.winfo_screenwidth()
        self.screen_height = self.parent.winfo_screenheight()
        self.cell_side_length = 10
        self.canvas_size = self.cell_side_length*len(grid)
        super(ResultFrame,self).__init__(parent,width=self.screen_width,height=self.screen_height)
        self.draw_and_save_result(grid)

        #Creates canvas based on grid. The canvas can be scrolled.
        canvas = Canvas(self,width=self.canvas_size,height=self.canvas_size,bg="#ddd",scrollregion=(0,0,self.canvas_size,self.canvas_size))
        hbar = Scrollbar(self, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=canvas.xview)
        vbar = Scrollbar(self, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)
        canvas.config(width=self.screen_width, height=self.screen_width)
        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        canvas.pack(side=TOP,fill=BOTH,padx=1,pady=1)
        parent.update_idletasks()
        self.board(canvas,grid)
        self.parent.after(5000, self.save_canvas(canvas))

    def board(self,view,grid):
        cols = len(grid)
        rows = len(grid)
        coordinate = {}
        rowNumber = 0
        for row in range(rows):
            columnNumber = 0
            rowNumber = rowNumber + 1
            for col in range(cols):
                columnNumber = columnNumber + 1

                if(type(grid[row][col]) is cellstates.FullCell):
                    fill = '#9bc146'
                elif(type(grid[row][col]) is cellstates.OnlyACell):
                    fill = '#ffe338'
                elif (type(grid[row][col]) is cellstates.OnlyBCell):
                    fill = '#ffa500'
                else:
                    fill = '#df1313'

                rect = view.create_rectangle(col * self.cell_side_length,
                                             row * self.cell_side_length,
                                             (col + 1) * self.cell_side_length,
                                             (row + 1) * self.cell_side_length,
                                             fill=fill)
                # Sets row, column
                view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                coordinate[(row, col)] = rect
        return coordinate

    def draw_and_save_result(self,grid):
        cols = len(grid)
        rows = len(grid)

        im = Image.new("RGB", (self.cell_side_length * cols,self.cell_side_length * rows))
        draw = ImageDraw.Draw(im)

        rowNumber = 0
        for row in range(rows):
            columnNumber = 0
            rowNumber = rowNumber + 1
            for col in range(cols):
                columnNumber = columnNumber + 1

                if(type(grid[row][col]) is cellstates.FullCell):
                    fill = "green"
                elif(type(grid[row][col]) is cellstates.OnlyACell):
                    fill = "orange"
                elif (type(grid[row][col]) is cellstates.OnlyBCell):
                    fill = "yellow"
                else:
                    fill = "red"

                draw.rectangle([col * self.cell_side_length,
                                      row * self.cell_side_length,
                                      (col + 1) * self.cell_side_length,
                                      (row + 1) * self.cell_side_length],fill,"black")

        filename = "hexholes_result"
        im.save(filename+".png")

        try:
            os.remove(filename+".ps")
        except OSError:
            pass

    def save_canvas(self, canvas):
        canvas.update()
        canvas.postscript(file="result.ps", colormode='color')

class WorkThread(threading.Thread):
    def __init__(self, queue, iterations, p1, p2, p3, full_p, only_p):
        self.iterations = iterations
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.full_p = full_p
        self.only_p = only_p
        self.loop = asyncio.get_event_loop()
        self.queue = queue
        threading.Thread.__init__(self)

    def run(self):
        self.loop.run_until_complete(self.do_iterations())

    @asyncio.coroutine
    def do_iterations(self):
        self.hexholeGrid = hexholegrid.Hexholegrid(self.queue, self.p1, self.p2, self.p3, self.full_p, self.only_p)
        self.hexholeGrid.perform_iterations(self.iterations)
        self.queue.put(("result", self.hexholeGrid.grid))

class HexholeApp(tk.Frame):
    def do_async_work(self,iterations,p1,p2,p3,full_p,only_p):
        self.parent.wm_state('iconic')
        self.results_toplevel = self.create_toplevel("Calculating hexholes")
        self.create_progress_label(self.results_toplevel,"Iterations completed {}/{}".format(0,iterations))
        self.start_progress_bar(iterations,self.results_toplevel)
        self.work_thread = None
        self.work_thread = WorkThread(self.queue, iterations,p1,p2,p3,full_p,only_p)
        self.parent.after(5000, self.check_queue())
        self.work_thread.start()

    def start_progress_bar(self, max, context):
        self.progress_bar = ttk.Progressbar(context, orient="horizontal", length=200, mode="determinate")
        self.progress_bar["maximum"] = max
        self.progress_bar["value"] = 0
        self.progress_bar.pack()

    def check_queue(self):
        if not self.work_thread.isAlive:
            return

        if self.queue.empty():
            self.parent.after(500, self.check_queue)
            return

        while not self.queue.empty():
            key, data = self.queue.get()
            if (key == "iteration"):
                self.progress_bar["value"] = self.progress_bar["maximum"] - data
                self.progress_label_text.set("Performing iteration {}/{}".format(self.progress_bar["value"],self.progress_bar["maximum"]))
            elif (key == "result"):
                self.clear_toplevel(self.results_toplevel)
                self.show_final_grid(self.results_toplevel,data)

        self.parent.after(1000, self.check_queue)

    def create_progress_label(self,context,text):
        self.progress_label_text = StringVar()
        self.progress_label = Label(context, textvariable=self.progress_label_text)
        self.progress_label.pack()
        self.progress_label_text.set(text)

    def create_toplevel(self,title):
        toplevel = Toplevel()
        toplevel.title = title
        return toplevel

    def clear_toplevel(self, toplevel):
        for widget in toplevel.winfo_children():
            widget.destroy()

    def show_final_grid(self, toplevel, grid):
        ResultFrame(toplevel,grid).pack(side="top", fill="both", expand=True)

    def __init__(self, parent):
        iterations_input = StringVar()
        p1_input = StringVar()
        p2_input = StringVar()
        p3_input = StringVar()
        full_input = StringVar()
        only_input = StringVar()
        self.queue = queue.Queue()
        self.parent = parent
        tk.Frame.__init__(self, parent)
        tk.Label(parent, text = "Number of iterations \n(Positive integer)").pack()
        tk.Entry(parent, textvariable = iterations_input).pack()
        tk.Label(parent, text="Probability 1 \n(Positive decimal number 1.0 or below)").pack()
        tk.Entry(parent, textvariable = p1_input).pack()
        tk.Label(parent, text="Probability 2 \n(Positive decimal number 1.0 or below)").pack()
        tk.Entry(parent, textvariable = p2_input).pack()
        tk.Label(parent, text="Probability 3 \n(Positive decimal number 1.0 or below)").pack()
        tk.Entry(parent, textvariable = p3_input).pack()
        tk.Label(parent, text="Probability Full to OnlyA/B \n(Positive decimal number 1.0 or below)").pack()
        tk.Entry(parent, textvariable = full_input).pack()
        tk.Label(parent, text="Probability OnlyA/B to Empty \n(Positive decimal number 1.0 or below)").pack()
        tk.Entry(parent, textvariable= only_input).pack()
        tk.Button(master=parent, text='Perform iterations', highlightbackground='#3E4149',
                  command=lambda: self.do_async_work(int(iterations_input.get()),float(p1_input.get()),float(p2_input.get()),float(p3_input.get()),float(full_input.get()),float(only_input.get()))).pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Hexholes')
    HexholeApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()