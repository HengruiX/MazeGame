import random
from Tkinter import *


class Cell:
    def __init__(self):
        self.walls = set()
        self.walls.add("n")
        self.walls.add("s")
        self.walls.add("e")
        self.walls.add("w")

    def is_clear(self, direction):
        return direction not in self.walls

    def remove_wall(self, direction):
        if direction in self.walls:
            self.walls.remove(direction)


class Maze:
    def __init__(self, length=20, width=15):
        self.grid = []
        self.length = length
        self.width = width
        for i in range(self.width):
            row = []
            for j in range(self.length):
                cell = Cell()
                row.append(cell)
            self.grid.append(row)

    def is_clear(self, x, y, direction):
        return self.grid[y][x].is_clear(direction)

    def is_out(self, x, y):
        return x >= self.length or y >= self.width or x < 0 or y < 0

    def paint(self, canvas):
        for i in range(self.width):
            for j in range(self.length):
                cell = self.grid[i][j]
                if not cell.is_clear("n"):
                    canvas.create_line(j * cell_side + padding, i * cell_side + padding,
                                       (j + 1) * cell_side + padding, i * cell_side + padding)
                if not cell.is_clear("s"):
                    canvas.create_line(j * cell_side + padding, (i + 1) * cell_side + padding,
                                       (j + 1) * cell_side + padding, (i + 1) * cell_side + padding)
                if not cell.is_clear("w"):
                    canvas.create_line(j * cell_side + padding, i * cell_side + padding,
                                       j * cell_side + padding, (i + 1) * cell_side + padding)
                if not cell.is_clear("e"):
                    canvas.create_line((j + 1) * cell_side + padding, i * cell_side + padding,
                                       (j + 1) * cell_side + padding, (i + 1) * cell_side + padding)


class Player:
    x = 0
    y = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, direction):
        global step_counter
        step_counter += 1
        if direction == "n":
            self.y -= 1
        elif direction == "s":
            self.y += 1
        elif direction == "e":
            self.x += 1
        elif direction == "w":
            self.x -= 1

    def paint(self, canvas):
        canvas.create_oval(padding + self.x * cell_side + cell_side / 2 - player_radius,
                           padding + self.y * cell_side + cell_side / 2 - player_radius,
                           padding + self.x * cell_side + cell_side / 2 + player_radius,
                           padding + self.y * cell_side + cell_side / 2 + player_radius,
                           fill=player_color)



def DFS_generate(maze, x=0, y=0):
    def generate(maze, x, y, xstack, ystack, visited):

        def all_visited(visited):
            for row in visited:
                for val in row:
                    if not val:
                        return False
            return True

        def get_opposite(direction):
            if direction == "n":
                return "s"
            if direction == "s":
                return "n"
            if direction == "e":
                return "w"
            if direction == "w":
                return "e"

        visited[y][x] = True
        if not all_visited(visited):
            directions = []
            if y - 1 >= 0 and not visited[y - 1][x]:
                directions.append("n")
            if x - 1 >= 0 and not visited[y][x - 1]:
                directions.append("w")
            if y + 1 < len(visited) and not visited[y + 1][x]:
                directions.append("s")
            if x + 1 < len(visited[y]) and not visited[y][x + 1]:
                directions.append("e")
            if len(directions) == 0:
                next_x = xstack.pop()
                next_y = ystack.pop()
                generate(maze, next_x, next_y, xstack, ystack, visited)
            else:
                direction = directions[random.randrange(len(directions))]
                next_x = x
                next_y = y
                if direction == "n":
                    next_y -= 1
                elif direction == "s":
                    next_y += 1
                elif direction == "e":
                    next_x += 1
                elif direction == "w":
                    next_x -= 1
                maze.grid[y][x].remove_wall(direction)
                maze.grid[next_y][next_x].remove_wall(get_opposite(direction))
                xstack.append(x)
                ystack.append(y)

                generate(maze, next_x, next_y, xstack, ystack, visited)

    if x == 0:
        maze.grid[y][x].remove_wall("w")
    elif x == len(maze.grid[y]) - 1:
        maze.grid[y][x].remove_wall("e")
    elif y == 0:
        maze.grid[y][x].remove_wall("n")
    elif y == len(maze.grid) - 1:
        maze.grid[y][x].remove_wall("s")

    visited = []
    for i in range(maze.width):
        row = []
        for j in range(maze.length):
            row.append(False)
        visited.append(row)
    xstack = []
    ystack = []
    generate(maze, x, y, xstack, ystack, visited)



def DFS_crazy_generate(maze, how_crazy = 0.1,x=0, y=0):
    def generate(maze, x, y, xstack, ystack, visited):

        def all_visited(visited):
            for row in visited:
                for val in row:
                    if not val:
                        return False
            return True

        def get_opposite(direction):
            if direction == "n":
                return "s"
            if direction == "s":
                return "n"
            if direction == "e":
                return "w"
            if direction == "w":
                return "e"

        visited[y][x] = True
        if not all_visited(visited):
            directions = []
            if y - 1 >= 0:
                if not visited[y - 1][x]:
                    directions.append("n")
                elif random.randrange(int(1 / how_crazy)) == 0:
                    visited[y - 1][x] = False
                    directions.append("n")
            if x - 1 >= 0:
                if not visited[y][x - 1]:
                    directions.append("w")
                elif random.randrange(int(1 / how_crazy)) == 0:
                    visited[y][x - 1] = False
                    directions.append("w")
            if y + 1 < len(visited):
                if not visited[y + 1][x]:
                    directions.append("s")
                elif random.randrange(int(1 / how_crazy)) == 0:
                    visited[y + 1][x] = False
                    directions.append("s")
            if x + 1 < len(visited[y]):
                if not visited[y][x + 1]:
                    directions.append("e")
                elif random.randrange(int(1 / how_crazy)) == 0:
                    visited[y][x + 1] = False
                    directions.append("e")
            if len(directions) == 0:
                next_x = xstack.pop()
                next_y = ystack.pop()
                generate(maze, next_x, next_y, xstack, ystack, visited)
            else:
                direction = directions[random.randrange(len(directions))]
                next_x = x
                next_y = y
                if direction == "n":
                    next_y -= 1
                elif direction == "s":
                    next_y += 1
                elif direction == "e":
                    next_x += 1
                elif direction == "w":
                    next_x -= 1
                maze.grid[y][x].remove_wall(direction)
                maze.grid[next_y][next_x].remove_wall(get_opposite(direction))
                xstack.append(x)
                ystack.append(y)
                try:
                    generate(maze, next_x, next_y, xstack, ystack, visited)
                except Exception:
                    return

    if x == 0:
        maze.grid[y][x].remove_wall("w")
    elif x == len(maze.grid[y]) - 1:
        maze.grid[y][x].remove_wall("e")
    elif y == 0:
        maze.grid[y][x].remove_wall("n")
    elif y == len(maze.grid) - 1:
        maze.grid[y][x].remove_wall("s")

    visited = []
    for i in range(maze.width):
        row = []
        for j in range(maze.length):
            row.append(False)
        visited.append(row)
    xstack = []
    ystack = []
    try:
        generate(maze, x, y, xstack, ystack, visited)
    except Exception:
        print "too crazy"
        return




def key_action(event):
    if win == False:
        if event.keycode == 8255233:
            if maze.grid[player.y][player.x].is_clear("s"):
                player.move("s")
                canvas.delete(ALL)
                maze.paint(canvas)
                player.paint(canvas)
        elif event.keycode == 8189699:
            if maze.grid[player.y][player.x].is_clear("e"):
                player.move("e")
                canvas.delete(ALL)
                maze.paint(canvas)
                player.paint(canvas)
        elif event.keycode == 8320768:
            if maze.grid[player.y][player.x].is_clear("n"):
                player.move("n")
                canvas.delete(ALL)
                maze.paint(canvas)
                player.paint(canvas)
        elif event.keycode == 8124162:
            if maze.grid[player.y][player.x].is_clear("w"):
                player.move("w")
                canvas.delete(ALL)
                maze.paint(canvas)
                player.paint(canvas)
        if maze.is_out(player.x, player.y):
            canvas.delete(ALL)
            victory(canvas)
    else:
        if event.keycode == 1179697:
            re_initialize(False, canvas)
        elif event.keycode == 1245234:
            re_initialize(True, canvas)
        elif event.keycode == 2359309:
            tk.destroy()


def victory(canvas):
    global win
    win = True
    text = "you win!\nyou used " + str(
        step_counter) + " step(s)\npress '1' to play again with the same maze, press '2' \nto change the maze, press 'enter' to quit the game"
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, text=text, justify="center")


def initialize(is_random=True, length=20, width=20):
    global step_counter
    global player
    global maze
    global win
    global randomize
    win = False
    randomize = is_random
    step_counter = 0
    maze = Maze(length, width)
    DFS_crazy_generate(maze, 0.01)
    if is_random:
        player = Player(random.randrange(maze.length), random.randrange(maze.width))
    else:
        player = Player(maze.length - 1, maze.width - 1)


def re_initialize(do_change, canvas):
    global step_counter
    global player
    global maze
    global win
    win = False
    step_counter = 0
    if do_change:
        maze = Maze(maze.length, maze.width)
        DFS_crazy_generate(maze, 0)
    if randomize:
        player = Player(random.randrange(maze.length), random.randrange(maze.width))
    else:
        player = Player(maze.length - 1, maze.width - 1)
    canvas.delete(ALL)
    maze.paint(canvas)
    player.paint(canvas)


cell_side = 20
padding = 5
player_radius = 4
trace_radius = 2
player_color = "red"
trace_color = "blue"
step_counter = 0
win = False
randomize = True

player = None
maze = None
initialize(False)

tk = Tk()
tk.title("maze")
canvas = Canvas(tk, width=cell_side * maze.length + 2 * padding,
                height=cell_side * maze.width + 2 * padding)
maze.paint(canvas)
player.paint(canvas)
canvas.focus_set()
canvas.bind("<Key>", key_action)
canvas.pack()
tk.mainloop()

