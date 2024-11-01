from manim import *
import random
from collections import deque

# Maze parameters
WIDTH, HEIGHT = 25, 25  # Width and height of the maze in cells
CELL_SIZE = 0.5
START, END = (0, 0), (WIDTH - 1, HEIGHT - 1)

def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]
    start_x, start_y = 0, 0
    maze[start_y][start_x] = 0
    walls = []

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = start_x + dx, start_y + dy
        if 0 <= nx < width and 0 <= ny < height:
            walls.append((nx, ny, dx, dy))

    while walls:
        wall = random.choice(walls)
        walls.remove(wall)
        nx, ny, dx, dy = wall
        opposite_x, opposite_y = nx + dx, ny + dy

        if 0 <= opposite_x < width and 0 <= opposite_y < height and maze[opposite_y][opposite_x] == 1:
            maze[ny][nx] = 0
            maze[opposite_y][opposite_x] = 0

            for ddx, ddy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                wall_x, wall_y = opposite_x + ddx, opposite_y + ddy
                if 0 <= wall_x < width and 0 <= wall_y < height and maze[wall_y][wall_x] == 1:
                    walls.append((wall_x, wall_y, ddx, ddy))

    maze[END[1]][END[0]] = 0
    return maze

def solve_maze_bfs(maze, start, end):
    visited = {}
    queue = deque([start])
    visited[start] = None

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            return backtrack_path(visited, start, end)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0 and (nx, ny) not in visited:
                visited[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    return None

def backtrack_path(visited, start, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = visited[current]
    path.reverse()
    return path

class MazeVisualization(ThreeDScene):  # Use ThreeDScene for 3D capabilities
    def construct(self):
        # Set up 3D camera to face the maze directly from above
        self.set_camera_orientation(phi=180 * DEGREES, theta=0 * DEGREES)

        # Generate the maze
        maze = generate_maze(WIDTH, HEIGHT)

        # Calculate the offset to center the maze
        x_offset = -WIDTH * CELL_SIZE / 2
        y_offset = -HEIGHT * CELL_SIZE / 2
        z_offset = 25  # Keep z_offset at 0 for a top-down view

        # Draw the maze
        squares = []
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                square = Square(side_length=CELL_SIZE)
                # Move squares in 3D space
                square.move_to(np.array([x * CELL_SIZE + x_offset, y * CELL_SIZE + y_offset, z_offset]))
                if cell == 1:
                    square.set_fill(BLACK, opacity=1)
                else:
                    square.set_fill(WHITE, opacity=1)
                squares.append(square)
                self.add(square)

        # Animate the maze drawing
        self.play(*[FadeIn(square) for square in squares], run_time=1)

        # Solve the maze
        path = solve_maze_bfs(maze, START, END)

        # Animate the path finding
        if path:
            path_squares = []
            for (x, y) in path:
                square = Square(side_length=CELL_SIZE)
                # Move path squares in 3D space
                square.move_to(np.array([x * CELL_SIZE + x_offset, y * CELL_SIZE + y_offset, z_offset + 0.1]))
                square.set_fill(RED, opacity=1)
                path_squares.append(square)
                self.play(FadeIn(square), run_time=0.1)

        # No need for 3D rotation since the view is fixed from above
        self.wait(2)
