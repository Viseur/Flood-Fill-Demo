def floodFill(x, y, grid_array, prevColor, newColor):

    # base cases:
    if (x < 0 or y < 0 or x >= len(grid_array) or y >= len(grid_array)
                            or
        grid_array[x][y] != prevColor or grid_array[x][y] == newColor):

        return

    grid_array[x][y] = newColor

    floodFill(x + 1, y, grid_array, prevColor, newColor)
    floodFill(x - 1, y, grid_array, prevColor, newColor)
    floodFill(x, y + 1, grid_array, prevColor, newColor)
    floodFill(x, y - 1, grid_array, prevColor, newColor)

def fill(x, y, grid, newColor):
    prevColor = grid[x][y]
    floodFill(x, y, grid, prevColor, newColor)
