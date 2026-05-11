  # TODO Test this and change Self to the way of version py 3.10
from abc import ABC, abstractmethod
from enum import Enum
from typing import overload, Any
from pydantic import BaseModel, Field, model_validator, ConfigDict
import sys
import random
import copy
from collections import deque


class MazeConfiguration(BaseModel):
    """Create a data-class with maze configuration data.

    Args:
        WIDTH (int): The width of the maze
        HEIGHT (int): The height of the maze
        ENTRY (tuple[int, int]): The entry point of the maze
        EXIT (tuple[int, int]): The exit point of the maze
        PERFECT (bool): If the maze has only one way to be completed
        SEED (float | None): The seed used to create the maze
        ALGORITHM (str): The algorithm wanted to create the maze
        EXTRA (dict[str, str] | None): Extra data for others special mazes
    """
    model_config = ConfigDict(frozen=True)

    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    PERFECT: bool = False
    SEED: float | None = None
    ALGORITHM: str | None = Field(max_length=255, default=None)
    EXTRA: dict[str, str] | None = None
    pass


class Maze(BaseModel):
    """Create a data-class with information of a Maze.

    ATTENTION this class isn't mean to be created outside. Unexpected errors
    could be raised on it's creation.

    It contains all the information need for the user about the Maze

    Args:
        maze_map: str
        entry: tuple[int, int]
        exit: tuple[int, int]
    """
    maze_map: str
    entry: tuple[int, int]
    exit: tuple[int, int]
    maze_solutions: list[str] = []

    @model_validator(mode="after")
    def set_solutions(self) -> "Maze":
        """Set the maze solution.

        Args:
            None (None): Nothing

        Returns:
            Self: Need for model_validator
        """
        if (len(self.maze_map) > 1056):
            self.maze_solutions = self.maze_solutioneer_shortest()  # cambiar
        else:
            self.maze_solutions = self.maze_solutioneer()
        return self

    def maze_solutioneer(self) -> list[str]:
        """
        Finds ALL possible paths from entry to exit without
        revisiting the same cell in a single path.
        Returns:
            list[str]: A list containing all the solution strings representing
            the sequence of movements (N, E, S, W).
        """
        grid = [[int(char, 16) for char in line]
                for line in self.maze_map.strip().split('\n')]
        height = len(grid)
        width = len(grid[0])
        start_x, start_y = self.entry
        end_x, end_y = self.exit

        directions = [
            (-1, 0, 1, 'N'),  # Norte: bit 1
            (0, 1, 2, 'E'),   # Este: bit 2
            (1, 0, 4, 'S'),   # Sur: bit 4
            (0, -1, 8, 'W')   # Oeste: bit 8
        ]

        all_paths = []
        current_path_visited = set()

        def f_recursive(y: int, x: int, path_str: str):

            if (y, x) == (end_y, end_x):
                all_paths.append(path_str)
                return

            current_path_visited.add((y, x))

            for dy, dx, wall_bit, char in directions:
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width:
                    if (not (grid[y][x] & wall_bit) and
                       (ny, nx) not in current_path_visited):
                        f_recursive(ny, nx, path_str + char)

            current_path_visited.remove((y, x))

        f_recursive(start_y, start_x, "")
        return all_paths

    def maze_solutioneer_shortest(self) -> list[str]:
        """
        Finds the shortest path from entry to exit
        using a Breadth-First Search (BFS).

        Returns:
            list[str]: A list containing a single string representing the
                    shortest sequence of movements (N, E, S, W).
        """
        grid = [[int(char, 16) for char in line]
                for line in self.maze_map.strip().split('\n')]
        height = len(grid)
        width = len(grid[0])
        start_x, start_y = self.entry
        end_x, end_y = self.exit

        directions = [
            (-1, 0, 1, 'N'),  # Norte: bit 1
            (0, 1, 2, 'E'),   # Este: bit 2
            (1, 0, 4, 'S'),   # Sur: bit 4
            (0, -1, 8, 'W')   # Oeste: bit 8
        ]
        queue: deque[tuple[int, int, str]] = deque([(start_y, start_x, "")])
        visited: set[tuple[int, int]] = set([(start_y, start_x)])

        while queue:
            curr_y, curr_x, path = queue.popleft()

            if (curr_y, curr_x) == (end_y, end_x):
                return [path]

            for dy, dx, wall_bit, char in directions:
                ny, nx = curr_y + dy, curr_x + dx

                if 0 <= ny < height and 0 <= nx < width:
                    if not (grid[curr_y][curr_x] & wall_bit):
                        if (ny, nx) not in visited:
                            visited.add((ny, nx))
                            queue.append((ny, nx, path + char))
        return []


class MazeGenerator(ABC):
    """The maze generator creator"""
    def __init__(self, config: MazeConfiguration) -> None:
        """
        Initializes the maze generator with a specific configuration.

        Args:
            config (MazeConfiguration): Data-class containing maze dimensions,
                entry/exit points, and the reproduction seed.
        """
        self.config = config
        self.rng = random.Random(self.config.SEED)
        self.skip_pattern = False
        self.validate_config()

    @abstractmethod
    def generate(self) -> Maze:
        """Generates a Maze object

        Returns:
            Maze: The Maze data-class with a Maze information
        """
        ...

    def validate_config(self) -> None:
        """
        Validates maze dimensions, entry/exit points, and checks if the
        dimensions are large enough to include the '42' pattern.
        """
        cnf = self.config
        if cnf.WIDTH <= 0 or cnf.HEIGHT <= 0:
            print("[ERROR] WIDTH and HEIGHT must be positive integers.")
            sys.exit(1)

        for (x, y) in [cnf.ENTRY, cnf.EXIT]:
            if not (0 <= x < cnf.WIDTH and 0 <= y < cnf.HEIGHT):
                print(f"[ERROR] ENTRY and EXIT must be within grid bounds: "
                      f"x in [0, {cnf.WIDTH}), y in [0, {cnf.HEIGHT})")
                sys.exit(1)

        if cnf.ENTRY == cnf.EXIT:
            print("[ERROR] ENTRY and EXIT must be different coordinates.")
            sys.exit(1)

        if cnf.WIDTH < 9 or cnf.HEIGHT < 7:
            print("[ERROR] Maze too small for '42' pattern. Omitting pattern.")
            self.skip_pattern = True

        if self.skip_pattern is False:
            xe, ye = self.config.ENTRY
            xx, yx = self.config.EXIT
            if ((ye, xe) or (yx, xx)) in self._get_42_coords():
                print("[ERROR]: Entry/Exit cells can't be "
                      "inside the 42 pattern.")
                sys.exit(1)

    def _get_42_coords(self) -> list[tuple[int, int]]:
        """
        Calculates the grid coordinates required to draw the '42' pattern.

        Returns:
            list[tuple[int, int]]: A list of (y, x) coordinates for
            fully closed cells.
        """

        mx = (self.config.WIDTH - 1) // 2
        my = (self.config.HEIGHT - 1) // 2
        coords: list[tuple[int, int]] = []

        # "4"
        coords.append((my - 2, mx - 3))
        coords.append((my - 2, mx - 1))
        coords.append((my - 1, mx - 3))
        coords.append((my - 1, mx - 1))
        coords.append((my, mx - 3))
        coords.append((my, mx - 1))
        coords.append((my, mx - 2))
        coords.append((my + 1, mx - 1))
        coords.append((my + 2, mx - 1))
        # "2"
        coords.append((my - 2, mx + 1))
        coords.append((my, mx + 1))
        coords.append((my + 1, mx + 1))
        coords.append((my + 2, mx + 1))
        coords.append((my - 2, mx + 2))
        coords.append((my, mx + 2))
        coords.append((my + 2, mx + 2))
        coords.append((my - 2, mx + 3))
        coords.append((my - 1, mx + 3))
        coords.append((my, mx + 3))
        coords.append((my + 2, mx + 3))

        return coords

    def _grid_to_hex_str(self, grid: list[list[int]]) -> str:
        """
        Converts the internal integer grid into the required
        hexadecimal string format.

        Args:
            grid (list[list[int]]): 2D list of integers representing
            cell wall states.

        Returns:
            str: A multi-line string with one hexadecimal digit per cell.
        """

        lines: list[str] = []
        for row in grid:
            hex_row = "".join([hex(cell)[2:].upper() for cell in row])
            lines.append(hex_row)
        return "\n".join(lines) + "\n"

    def _add_loops(self, grid: list[list[int]],
                   ft_pattern: list[list[bool]]) -> None:
        """
        Adds cycles to the maze by removing L extra walls
        between adjacent cells.

        Args:
            grid (list[list[int]]): The maze grid to modify.
            ft_pattern (list[list[bool]]): Matrix where True is a '42' cell.
        """
        MOVEMENTS: dict[str, tuple[int, int, int, int]] = {
            "E": (0, 1, -2, -8),
            "S": (1, 0, -4, -1),
            "W": (0, -1, -8, -2),
            "N": (-1, 0, -1, -4)
        }

        L = max(1, int((self.config.WIDTH * self.config.HEIGHT) * 0.02))  # probar y cambiar si hace falta. igual hacer distinción labs pequeños/grandes
        extra_corrs = 0
        while extra_corrs < L:
            y = self.rng.randint(0, self.config.HEIGHT - 1)
            x = self.rng.randint(0, self.config.WIDTH - 1)
            if ft_pattern[y][x]:
                continue

            valid_neighbours = []
            for direction, (dy, dx, c_w, n_w) in MOVEMENTS.items():
                ny, nx = y + dy, x + dx
                if (0 <= ny < self.config.HEIGHT
                   and 0 <= nx < self.config.WIDTH):
                    if not ft_pattern[ny][nx]:
                        if grid[y][x] & abs(c_w):
                            valid_neighbours.append((ny, nx, c_w, n_w))

            if valid_neighbours:
                ny, nx, c_w, n_w = self.rng.choice(valid_neighbours)
                grid[y][x] += c_w
                grid[ny][nx] += n_w
                extra_corrs += 1


class DFSMazeGenerator(MazeGenerator):
    """
    Maze generator that implements the Depth-First Search (DFS) algorithm,
    also known as the Recursive Backtracker.
    This generator produces perfect mazes by carving paths into a grid of
    fully closed cells, ensuring full connectivity without loops.

    Attributes:
        MOVEMENTS (dict): Mapping of cardinal directions to grid deltas and
        bitwise wall removal values (N=1, E=2, S=4, W=8).
    """
    MOVEMENTS: dict[str, tuple[int, int, int, int]] = {
            "E": (0, 1, -2, -8),
            "S": (1, 0, -4, -1),
            "W": (0, -1, -8, -2),
            "N": (-1, 0, -1, -4)
    }

    def _run_dfs(self, grid: list[list[int]],
                 visited: list[list[bool]]) -> None:
        """
        Executes the Recursive Backtracker algorithm using a stack.
        This method modifies the grid in-place by removing bits from the cell
        values to open paths between neighbours.

        Args:
            grid (list[list[int]]): The grid to be modified.
            visited (list[list[bool]]): Matrix to track visited cells.
        """

        start_x, start_y = self.config.ENTRY
        stack = [(start_y, start_x)]
        visited[start_y][start_x] = True

        while stack:
            curr_y, curr_x = stack[-1]
            neighbours = []
            for direction, (dy, dx, c_wall, n_wall) in self.MOVEMENTS.items():
                ny, nx = curr_y + dy, curr_x + dx
                if (0 <= ny < self.config.HEIGHT
                   and 0 <= nx < self.config.WIDTH):
                    if not visited[ny][nx]:
                        neighbours.append((ny, nx, c_wall, n_wall))
            if neighbours:
                ny, nx, c_wall, n_wall = self.rng.choice(neighbours)
                grid[curr_y][curr_x] += c_wall
                grid[ny][nx] += n_wall
                visited[ny][nx] = True
                stack.append((ny, nx))
            else:
                stack.pop()

    def generate(self) -> Maze:
        """
        Orchestrates the maze generation process.
        Initializes the grid, reserves the '42' pattern area, runs the DFS
        algorithm, and packages the result into a Maze object.

        Returns:
            Maze: The completed maze object containing the map and metadata.
        """
        grid = [[0xF for _ in range(self.config.WIDTH)]
                for _ in range(self.config.HEIGHT)]
        visited = [[False for _ in range(self.config.WIDTH)]
                   for _ in range(self.config.HEIGHT)]

        if not self.skip_pattern:
            for y, x in self._get_42_coords():
                if 0 <= y < self.config.HEIGHT and 0 <= x < self.config.WIDTH:
                    visited[y][x] = True
        ft_pattern = copy.deepcopy(visited)
        self._run_dfs(grid, visited)

        if not self.config.PERFECT:
            self._add_loops(grid, ft_pattern)

        return Maze(
            maze_map=self._grid_to_hex_str(grid),
            entry=self.config.ENTRY,
            exit=self.config.EXIT
        )


class GTMazeGenerator(DFSMazeGenerator):
    """
    Growing Tree Generator.
    Inherits movements and utility methods from DFSMazeGenerator.
    """
    def _run_growing_tree(self, grid: list[list[int]],
                          visited: list[list[bool]]) -> None:
        start_x, start_y = self.config.ENTRY
        active_cells = [(start_y, start_x)]
        visited[start_y][start_x] = True
        steps_in_current_path = 0
        curr_y, curr_x = start_y, start_x

        while active_cells:
            if steps_in_current_path >= 4:
                idx = self.rng.randint(0, len(active_cells) - 1)
                curr_y, curr_x = active_cells[idx]
                steps_in_current_path = 0
            else:
                curr_y, curr_x = active_cells[-1]

            neighbours = []
            for direction, (dy, dx, c_w, n_w) in self.MOVEMENTS.items():
                ny, nx = curr_y + dy, curr_x + dx
                if (0 <= ny < self.config.HEIGHT
                   and 0 <= nx < self.config.WIDTH):
                    if not visited[ny][nx]:
                        neighbours.append((ny, nx, c_w, n_w))

            if neighbours:
                ny, nx, c_w, n_w = self.rng.choice(neighbours)
                grid[curr_y][curr_x] += c_w
                grid[ny][nx] += n_w
                visited[ny][nx] = True
                active_cells.append((ny, nx))
                steps_in_current_path += 1
            else:
                active_cells.remove((curr_y, curr_x))
                steps_in_current_path = 4

    def generate(self) -> Maze:
        """
        Overrides the generate method to use Growing Tree instead of DFS.
        Returns:
            Maze: The completed maze object containing the map and metadata.
        """
        grid = [[0xF for _ in range(self.config.WIDTH)]
                for _ in range(self.config.HEIGHT)]
        visited = [[False for _ in range(self.config.WIDTH)]
                   for _ in range(self.config.HEIGHT)]

        if not self.skip_pattern:
            for y, x in self._get_42_coords():
                if 0 <= y < self.config.HEIGHT and 0 <= x < self.config.WIDTH:
                    visited[y][x] = True
        ft_pattern = copy.deepcopy(visited)
        self._run_growing_tree(grid, visited)

        if not self.config.PERFECT:
            self._add_loops(grid, ft_pattern)

        return Maze(
            maze_map=self._grid_to_hex_str(grid),
            entry=self.config.ENTRY,
            exit=self.config.EXIT
        )


class Algorithms(Enum):
    """A enumerator class for enumarating all possible Algorithms"""
    DFS = DFSMazeGenerator
    GT = GTMazeGenerator
    pass


class MazeGeneratorFactory(BaseModel):
    """Instance used for creating Maze Generators"""

    @overload
    @staticmethod
    def create_generator(
        CONFIG: MazeConfiguration = Field()
    ) -> MazeGenerator:
        """Creates the appropiate maze generator

        If any configuration value is impossible, an exception will be raised.
        Of course, if a Algorithm set doesn't exist, an exception will be
        raised.

        #  TODO devir a zeta que complete esto de abajo
        Algorithms (Note that that algorithm string is case insensitive):
            - DFS: The default algorithm...

        Args:
            config (MazeConfiguration): The MazeConfiguration data-class used
                to create the appropiate maze

        Returns:
            MazeGenerator: The MazeGenerator object.
        """
        ...

    @overload
    @staticmethod
    def create_generator(
        WIDTH: int = Field(),
        HEIGHT: int = Field(),
        ENTRY: tuple[int, int] = Field(),
        EXIT: tuple[int, int] = Field(),
        PERFECT: bool = Field(default=False),
        SEED: float | None = Field(default=None),
        ALGORITHM: str | None = Field(max_length=255, default=None),
        EXTRA: dict[str, str] | None = Field(default=None)
    ) -> MazeGenerator:
        """Creates the appropiate maze generator

        If any configuration value is impossible, an exception will be raised.
        Of course, if a Algorithm set doesn't exist, an exception will be
        raised.

        #  TODO devir a zeta que complete esto de abajo
        Algorithms (Note that that algorithm string is case insensitive):
            - DFS: The default algorithm...

        Args:
            WIDTH (int): The width of the maze
            HEIGHT (int): The height of the maze
            ENTRY (tuple[int, int]): The entry point of the maze
            EXIT (tuple[int, int]): The exit point of the maze
            PERFECT (bool): If the maze has only one way to be completed
            SEED (float | None): The seed used to create the maze
            ALGORITHM (str): The algorithm wanted to create the maze
            EXTRA (dict[str, str] | None): Extra data for others special mazes

        Returns:
            MazeGenerator: The MazeGenerator object.
        """
        ...

    @staticmethod
    def create_generator(
        *args: Any,
        **kwargs: Any
    ) -> MazeGenerator:
        """Creates the appropiate maze generator"""
        if len(args) == 1:
            config = args[0]
        else:
            config = MazeConfiguration(**kwargs)

        if config.ALGORITHM:
            for algorithm in Algorithms:
                if algorithm.name.lower() == config.ALGORITHM.lower():
                    return algorithm.value(config)
            raise ValueError("This algorithm doesn't exist")
        return DFSMazeGenerator(config)
