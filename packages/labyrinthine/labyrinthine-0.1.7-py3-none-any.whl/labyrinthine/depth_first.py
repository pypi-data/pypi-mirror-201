import random

from types import NoneType
from typing import List, Tuple, Union


def compute_neighbors(matrix: List[List[int]], cell: Tuple[int, int]) -> list[int]:
    result = []
    x, y = cell
    max_width, max_height = len(matrix), len(matrix[0])
    if x + 2 < max_width:
        result += [(x + 2, y)]
    if x - 2 >= 0:
        result += [(x - 2, y)]
    if y + 2 < max_height:
        result += [(x, y + 2)]
    if y - 2 >= 0:
        result += [(x, y - 2)]

    result = [cell for cell in result if matrix[cell[0]][cell[1]]]

    return result


def compute_wall(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    x1, y1 = a
    x2, y2 = b

    if x1 == x2:
        return x1, min(y1, y2) + 1
    else:
        return min(x1, x2) + 1, y1


def depth_first(size: int | Tuple[int, int], start: Tuple[int, int] = (0, 0),
                seed: Union[NoneType, int, float, str, bytes, bytearray] = None) \
        -> List[List[int]]:
    if isinstance(size, int):
        size = (size, size)

    random.seed(seed)

    width, height = size
    maze = [[1 for _ in range(width)] for _ in range(height)]
    stack = []

    # 1. Choose the initial cell, mark it as visited and push it to the stack
    cell = start
    maze[cell[0]][cell[1]] = 0

    stack += [cell]
    # 2. While the stack is not empty
    while stack:
        # 1. Pop a cell from the stack and make it a current cell
        cell = stack.pop()
        neighbors = compute_neighbors(maze, cell)
        # 2. If the current cell has any neighbours which have not been visited
        if neighbors:
            # 1. Push the current cell to the stack
            stack += [cell]
            # 2. Choose one of the unvisited neighbours
            neighbor = random.choice(neighbors)
            # 3. Remove the wall between the current cell and the chosen cell
            wall = compute_wall(cell, neighbor)
            maze[wall[0]][wall[1]] = 0
            # 4. Mark the chosen cell as visited and push it to the stack
            maze[neighbor[0]][neighbor[1]] = 0
            stack += [neighbor]

    return maze
