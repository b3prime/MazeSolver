from PIL import Image, ImageDraw

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class Frontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def taxiCab(self, node, goal):
        return abs(goal[1] - node.state[1]) + abs(goal[0] - node.state[0])

    def remove(self, goal):
        bestDist = 9999
        bestNode = None
        for node in self.frontier:
            dist = self.taxiCab(node, goal)
            if(dist < bestDist):
                bestDist = dist
                bestNode = node
        self.frontier.remove(bestNode)
        return bestNode
    
    def contains_state(self, state):
        if any(node.state == state for node in self.frontier):
            return True
        return False
    
    def empty(self):
        if len(self.frontier) == 0:
            return True

class Maze():
    def __init__(self, filename):
        with open(filename) as file:
            self.contents = file.read()

            if self.contents.count("A") > 1:
                raise Exception("Only one Start point!")
            if self.contents.count("B") > 1:
                raise Exception("Only one End point!")

            # determine length and height of maze
            self.contents = self.contents.splitlines()
            self.height = len(self.contents)
            self.width = max([len(line) for line in self.contents])

            # determine where the walls are
            # also, where start and end points are
            self.walls = []
            for i, line in enumerate(self.contents):
                arr = []
                for j, char in enumerate(line):
                    if (char) == "A":
                        self.start = (i, j)
                        arr.append(False)
                    elif (char) == "B":
                        self.goal = (i,j)
                        arr.append(False)
                    elif (char) == " ":
                        arr.append(False)
                    else:
                        arr.append(True)
                self.walls.append(arr)

    def neighbors(self, state):
        #find all possible next-moves from a certain state
        row, col = state
        candidates = [("up", (row-1, col)),
                    ("down", (row+1, col)),
                    ("left", (row, col-1)),
                    ("right", (row, col+1))
                    ]
        result = []

        # check if each candidate is within the maze, and isn't a wall
        for action, (r,c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r,c)))
        return result

    def solve(self, frontier):
        start = Node(self.start, parent=None, action=None)
        frontier.add(start)
        self.explored = set() #we don't want to search already-explored nodes!

        while True:
            if frontier.empty():
                raise Exception("No Solution")

            #remove node from frontier
            node = frontier.remove(self.goal)

            #check if goal state has been reached
            if node.state == self.goal:
                print("goal state reached...")
                actions = []
                cells = []
                while node.parent is not None: #continue backtracking through the tree
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse() #transforms from end->start to start->end
                cells.reverse() # ^
                return (actions, cells)
            
            self.explored.add(node.state)

            #determine the possible next-moves
            # next-move can't already be in the frontier and not explored
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
        
    def drawMaze(self):
        cellSize = 50
        img = Image.new(
                        "RGBA",
                        (self.width * cellSize, self.height * cellSize),
                        (0, 0, 0, 0)
                        )
        
        draw = ImageDraw.Draw(img)

        for i in range(self.height):
            for j in range(self.width):
                char = self.contents[i][j]
                if char == "B":
                    self.fill = (255, 0, 0)
                elif char == "A":
                    self.fill = (0, 255, 0)
                elif (i, j) in cells:
                    self.fill = (100, 100, 100)
                elif char == " ":
                    self.fill = (255, 255, 255)
                else:
                    self.fill = (0, 0, 0)
                draw.rectangle([((j*cellSize), (i*cellSize)),
                                (((j+1)*cellSize), ((i+1)*cellSize))],
                                fill=self.fill,
                                outline = (100,100,100)
                            )

        img.save("mazeOutput.png")

#EDIT PARAMETERS HERE!
maze = Maze("maze5.txt")
frontier = Frontier()

solution = maze.solve(frontier)
print(solution[0])

cells = solution[1]
maze.drawMaze()