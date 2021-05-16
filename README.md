# Flood-Fill-Demo
![image](https://user-images.githubusercontent.com/84274916/118399282-1f295580-b67a-11eb-831f-60238c58b04e.png)

A sample program, that fills a section on the canvas with a selected color, using the 4 - direction approach with recursive checks.
The program is written in pure Python, using Tkinter for the Interface, and PIL.

# How does the program work?
The program, instead of drawing native tkinter canvas lines, renders rectangles on mouse motion, in a grid that is created at program start up. When drawing, the program keeps track of active color and tool, and just for presentation purposes, also shows mouse coordinates, all at the left side of the screen.

![image](https://user-images.githubusercontent.com/84274916/118399449-cb6b3c00-b67a-11eb-847c-b11605fbef2f.png)

The program even has a **Tools** menu, that lets the user choose between the following tools:
1. Brush Tool
2. Eraser Tool
3. Fill Tool
4. Colors Menu (lets the user choose an active color)

and just for presentation again, it has a **Clear Canvas** option as well.
NOTE: The program uses tkinter's `colorchooser` module for the colors' dialog.

# Implementing the Flood fill functionality:
Of course, the main part of the program is its ability to fill a section of the program with an Active Color.
On startup, when the program renders the grid on the canvas, it records all the nodes on the canvas in this example form:

`
grid = {
(x1,y2) : 'black',
(x2,y2) : 'white'
}
`

wherein, `x,y` are the cell's row and column respectively.

Whilst drawing, the program simply replaces the current cell's color with the active color - both, on the canvas, as well as in the grid dictionary. Similarly, when performing the flood fill, it checks the nodes around by referring to the grid dictionary, or `dict` in python.

The flood fill algorithm is implemented quite simply, by grabbing the cell clicked when the current tool is the fill tool, and recursively check the color of the nodes around the clicked node. It colors only those nodes, which are the same color as the clicked node.

Checking the color of the clicked node is done by using PIL's `ImageGrab.grab()`, and then using the hex value of the color returned by using `grab()`. I defined a helper function for this, namely, `rgb_to_hex16`.

# References:
Theory: https://en.wikipedia.org/wiki/Flood_fill
Python implementation: https://www.geeksforgeeks.org/flood-fill-algorithm-implement-fill-paint/

NOTE: The program has a text based version as well, that is nearly the same as the one mentioned in the 'Python implementation' above, but it was my first attempt to writing flood fill algorithm in code.
