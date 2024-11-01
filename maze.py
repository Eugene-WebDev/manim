import random
from PIL import Image, ImageDraw
from collections import deque

# Maze parameters
WIDTH, HEIGHT = 25, 25  # Width and height of the maze in cells
CELL_SIZE = 25          # Size of each cell in pixels
START, END = (0, 0), (WIDTH - 1, HEIGHT - 1)  # Start and end points of the maze

def generate_maze(width, height):
    # Initialize maze with walls
    maze = [[1] * width for _ in range(height)]
    
    # Start at the top-left corner and mark it as a path
    start_x, start_y = 0, 0
    maze[start_y][start_x] = 0

    # List to keep track of walls
    walls = []

    # Add walls of the starting cell to the wall list
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = start_x + dx, start_y + dy
        if 0 <= nx < width and 0 <= ny < height:
            walls.append((nx, ny, dx, dy))  # (cell coordinates, wall direction)

    while walls:
        # Choose a random wall from the wall list
        wall = random.choice(walls)
        walls.remove(wall)

        nx, ny, dx, dy = wall
        opposite_x, opposite_y = nx + dx, ny + dy

        # Check if the opposite cell is a wall
        if 0 <= opposite_x < width and 0 <= opposite_y < height and maze[opposite_y][opposite_x] == 1:
            # Remove the wall and make the cell a path
            maze[ny][nx] = 0
            maze[opposite_y][opposite_x] = 0

            # Add the walls of the new cell to the wall list
            for ddx, ddy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                wall_x, wall_y = opposite_x + ddx, opposite_y + ddy
                if 0 <= wall_x < width and 0 <= wall_y < height and maze[wall_y][wall_x] == 1:
                    walls.append((wall_x, wall_y, ddx, ddy))

    # Ensure the end point is a path
    maze[END[1]][END[0]] = 0

    # Debugging: Print the maze to verify paths
    print("Maze after generation:")
    for row in maze:
        print("".join([' ' if cell == 0 else '#' for cell in row]))

    return maze


def is_valid_move(maze, x, y):
    return 0 <= x < len(maze[0]) and 0 <= y < len(maze) and maze[y][x] == 0

def backtrack_path(visited, start, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = visited[current]
    path.reverse()  # Reverse the path to go from start to end
    return path
def solve_maze_bfs(maze, start, end):
    visited = {}
    queue = deque([start])  # Initialize the queue with the starting point
    visited[start] = None  # Mark the start position as visited

    while queue:
        x, y = queue.popleft()  # Dequeue the next cell

        # Check if we've reached the end
        if (x, y) == end:
            return backtrack_path(visited, start, end)

        # Explore neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, down, left, right
            nx, ny = x + dx, y + dy
            if is_valid_move(maze, nx, ny) and (nx, ny) not in visited:
                visited[(nx, ny)] = (x, y)  # Mark the parent cell
                queue.append((nx, ny))  # Enqueue the neighbor
                print(f"Visiting: {(nx, ny)}")  # Debugging output

    return None  # Return None if no path is found

# Image generation
def draw_maze(maze, path=None):
    width, height = int(len(maze[0]) * CELL_SIZE), int(len(maze) * CELL_SIZE)  # Convert to integers
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Draw the maze
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = 'black' if cell == 1 else 'white'
            draw.rectangle([x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE], fill=color)

    # Draw the solution path in red
    if path:
        for x, y in path:
            draw.rectangle(
                [x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE],
                fill='red'
            )

    return image

# Main script
maze = generate_maze(WIDTH, HEIGHT)

# Debugging: Print the generated maze
print("Generated Maze:")
for row in maze:
    print("".join([' ' if cell == 0 else '#' for cell in row]))

# Print the start and end points
print(f"Start: {START}, End: {END}")

# Check if start and end points are valid
if maze[START[1]][START[0]] != 0:
    print("Start point is not a path!")
if maze[END[1]][END[0]] != 0:
    print("End point is not a path!")
else:
    print("Both start and end points are valid paths.")


# Solve the maze using BFS
path = solve_maze_bfs(maze, START, END)

# Debugging: Print the path or no path found
if path:
    print("Path found:", path)
else:
    print("No path found.")

# If a solution path was found, save the maze and solution as images
if path:
    maze_image = draw_maze(maze)
    maze_image.save("maze.png")
    
    solution_image = draw_maze(maze, path)
    solution_image.save("maze_with_solution.png")
    print("Maze and solution images have been saved.")
else:
    print("Error: No solution found, but this should be unlikely with the new generation method.")

