from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import ImageGrab

def getcell(mouseX, mouseY, gridSize):
    #gets cell info in grid
    return (((mouseX // gridSize)+1),((mouseY // gridSize)+1))

def rgb_to_hex_16(rgb):
    #helper function to return hex code of an rgb color
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

class FloodFillDemo:
    def __init__(self, master):
        self.master = master

        self.master.wm_attributes('-fullscreen',True)

        #some helper variables.
        self.gridSize = 0
        self.grid = {}

        self.colors = [rgb_to_hex_16((0,0,0)),rgb_to_hex_16((255,255,255))] #colors chosen by the user at some point in the program.

        self.i, self.j = [], []

        self.activeColor = rgb_to_hex_16((255,255,255))

        self.font=("Consolas", 12, 'normal')

        self.visited = []

        #draws the canvas onto the window.
        self.canvas = Canvas(self.master, height = 600 - 4, width = 600 - 4, bg="Black")
        self.canvas.pack(side=TOP)

        self.canvas.grid_propagate(False)

        self.master.update()
        
        self.currentStats()
        
        self.ch, self.cw = self.canvas.winfo_height(), self.canvas.winfo_width()
        self.eventHandler()
        self.createMenus()

        self.createGrid(20)
        
    def createMenus(self):
        self.masterMenu = Menu(self.master)

        self.master.config(bg="black")

        self.toolMenu = Menu(self.masterMenu, tearoff = 0)

        self.toolMenu.add_command(label = "Brush",  command = self.toggleBrush)
        self.toolMenu.add_command(label = "Fill",   command = self.toggleFillTool)
        self.toolMenu.add_command(label = "Eraser", command = self.toggleEraser)
        self.toolMenu.add_command(label = "Colors .. ", command = self.toggleColors)
        self.toolMenu.add_command(label = "Clear Canvas .. ", command = self.clearCanvas)

        self.masterMenu.add_cascade(label = "Tools ..", menu = self.toolMenu)

        self.master.config(menu = self.masterMenu)

    def currentStats(self):

        self.currentColorText = Label(self.master, text = "Active Color-> ", font=self.font, fg="white",bg="black")
        self.currentColorText.place(x=10, y=200)
        
        self.currentColorUI   = Label(self.master,text="###",fg=self.activeColor,font=self.font,bg="black")
        self.currentColorUI.place(x=170, y=200)

        self.coords = Label(self.master, text="Mouse-> (None, None)",font=self.font, fg="white",bg="black")
        self.coords.place(x=10, y=230)

        self.currentTool = Label(self.master, text = "Tool-> Brush", font=self.font, fg = "white", bg="black")
        self.currentTool.place(x=10, y = 260)

    def updateMouseCoords(self, event):
        self.coords.config(text = f"Mouse-> ({event.x},{event.y})")

    def toggleBrush(self):
        self.currentTool.config(text = "Tool-> Brush")

        self.canvas.bind("<B1-Motion>",self.onDrag)
        self.canvas.bind("<Button-1>",self.onDrag)
        
    def toggleFillTool(self):
        self.currentTool.config(text = "Tool-> Fill Tool")

        self.canvas.bind("<Button-1>",self.onClickFill)
        self.canvas.bind("<B1-Motion>",lambda e:"break")
        
    def toggleEraser(self):
        self.currentTool.config(text = "Tool-> Eraser")

        self.canvas.bind("<B1-Motion>",self.onDragErase)
        self.canvas.bind("<Button-1>",self.onDragErase)

    def toggleColors(self):
        currentColorChosen = askcolor()[-1] # choose hex value.
        self.activeColor = currentColorChosen

        self.currentColorUI.config(fg=self.activeColor)

        if self.activeColor != rgb_to_hex_16((0,0,0)):
            self.colors.append(self.activeColor)

        self.toggleBrush()

    def eventHandler(self):
        # handles canvas events.
        self.canvas.bind("<B1-Motion>",self.onDrag)
        self.canvas.bind("<Button-1>",self.onDrag)

        self.master.bind("<Control-g>", self.getVisitedNodes)
        self.master.bind("<Control-G>", self.getVisitedNodes)

        self.master.bind("<Motion>", self.updateMouseCoords)
        self.master.bind("<Escape>", lambda e:self.master.destroy())

    def getVisitedNodes(self, e):
        self.visited = list(set(self.visited))
        print(sorted(self.visited))
        
    def createGrid(self, gridSize):
        if gridSize >= 20:
        
            self.gridSize = gridSize

            for i in range(gridSize, self.cw-4, gridSize):
                self.canvas.create_line(i, 0, i, self.ch, tag = "gridLine")
                self.i.append(i)

            for j in range(gridSize, self.ch-4, gridSize):
                self.canvas.create_line(0, j, self.cw, j, tag = "gridLine")
                self.j.append(j)
        else:
            raise ValueError("Needed a value >= 10. ")

        for x in self.i:
            for y in self.j:
                self.grid[(x // self.gridSize, y // self.gridSize)] = rgb_to_hex_16((0,0,0))

    def clearCanvas(self):
        self.canvas.delete('pix')

        for i, j in self.grid.items():
            self.grid[i] = rgb_to_hex_16((0,0,0))

    def drawPix(self, cx, cy, activeColor):
        self.canvas.create_rectangle((cx-1) * self.gridSize, (cy-1)*self.gridSize,
                                     (cx)* self.gridSize, (cy)*self.gridSize,
                                     fill = activeColor, tag="pix")

    def onDrag(self, e):
        cell = getcell(e.x, e.y, self.gridSize)
        self.drawPix(cell[0], cell[1], self.activeColor)
        self.grid[cell] = self.activeColor

    def onDragErase(self, e):
        cell = getcell(e.x, e.y, self.gridSize)
        self.grid[cell] = rgb_to_hex_16((0,0,0)) # black stands for an empty node.
        self.drawPix(cell[0], cell[1], rgb_to_hex_16((0,0,0)))

    def run(self):
        self.master.mainloop()

    def updateGrid(self,):
        for i, j in self.grid.items():
            self.drawPix(i[0], i[1], j)

    def floodFillUtil(self, x, y, gridArray, prevColor, newColor):
        try:
            if (str(gridArray[(x,y)]) != prevColor or str(gridArray[(x,y)]) == newColor):
                # do not execute the program further.
                return
            gridArray[(x,y)] = newColor
            self.floodFillUtil(x + 1, y, gridArray, prevColor, newColor) ; self.visited.append((x,y))
            self.floodFillUtil(x - 1, y, gridArray, prevColor, newColor) ; self.visited.append((x,y))
            self.floodFillUtil(x, y + 1, gridArray, prevColor, newColor) ; self.visited.append((x,y))
            self.floodFillUtil(x, y - 1, gridArray, prevColor, newColor) ; self.visited.append((x,y))
            
        except:
            gridArray[(0,0)] = newColor
            gridArray[(x,y)] = newColor
            gridArray[(self.cw//self.gridSize,self.ch//self.gridSize)] = newColor

    def getColor(self, x, y):
        dx, dy = self.canvas.winfo_rootx() + x, self.canvas.winfo_rooty() + y
        return rgb_to_hex_16(ImageGrab.grab((dx, dy, dx + 1, dy + 1)).getpixel((0, 0))) # 1 pixel image.

    def floodFill(self, x, y, grid, prevColor, newColor):
        self.floodFillUtil(x, y, grid, prevColor, newColor)
        self.updateGrid()

    def onClickFill(self, e):
        cell = getcell(e.x, e.y, self.gridSize)
        self.floodFill(cell[0], cell[1], self.grid, self.getColor(e.x, e.y), self.activeColor)

def main():
    root=Tk()

    app = FloodFillDemo(root)
    app.run() 
        
if __name__ == "__main__": main()
