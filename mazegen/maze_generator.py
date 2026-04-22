
from abc import ABC, abstractmethod
from enum import Enum
from typing import overload, Self, Any
from pydantic import BaseModel, Field, model_validator, ConfigDict
import sys
import random
import copy


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

    WIDTH: int = Field()
    HEIGHT: int = Field()
    ENTRY: tuple[int, int] = Field()
    EXIT: tuple[int, int] = Field()
    PERFECT: bool = Field(default=False)
    SEED: float | None = Field(default=None)
    ALGORITHM: str | None = Field(max_length=255, default=None)
    EXTRA: dict[str, str] | None = Field(default=None)
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
    model_config = ConfigDict(frozen=True)

    maze_map: str = Field()
    entry: tuple[int, int] = Field()
    exit: tuple[int, int] = Field()
    maze_solutions: list[str] = Field(init=False)

    @model_validator(mode="after")
    def set_solutions(self) -> Self:
        """Set the maze solution.

        Args:
            None (None): Nothing

        Returns:
            Self: Need for model_validator
        """
        object.__setattr__(self, "maze_solutions", self.maze_solutioneer())
        return self

    def maze_solutioneer(self, maze_solutions: str | None = None) -> list[str]:  # TODO this method
        """Find the different paths to complete de maze.

        Returns:
            list[str]: A list with the solutions of the maze

        Raises:
        """
        return []
    pass


class MazeGenerator(ABC):
    """The maze generator creator"""
    def __init__(self, config: MazeConfiguration) -> None:
        """This is just the signature of a Maze Generator init"""
        self.config = config

        try:
            self.validate_config()
        except Exception as err:
            print(f"[ERROR]: {err}")
            sys.exit(1)
        return

    @abstractmethod
    def generate(self) -> Maze:
        """Generates a Maze object

        Returns:
            Maze: The Maze data-class with a Maze information
        """
        ...

    @abstractmethod
    def validate_config(self) -> None:
        """Validates if maze can be created with the actual configuration"""
        ...
    pass


class ExampleMazeGenerator(MazeGenerator):  # !! BORRAR ANTES DE ENTREGAR
    def __init__(self, config: MazeConfiguration) -> None:
        super().__init__(config)
        return

    def generate(self) -> Maze:
        return Maze(maze_map="Hola", entry=(1, 1), exit=(16, 2))

    def validate_config(self) -> None: ...
    pass


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

    def __init__(self, config: MazeConfiguration) -> None:
        """
        Initializes the DFS generator with a specific configuration.

        Args:
            config (MazeConfiguration): Data-class containing maze dimensions,
                entry/exit points, and the reproduction seed.
        """
        super().__init__(config)
        self.rng = random.Random(self.config.SEED)
        self.skip_pattern = False
        self.validate_config()

    def validate_config(self) -> None:
        """
        Checks if the maze dimensions are large enough to include the '42'
        pattern. According to the subject, if the maze is too small, the
        pattern is omitted and an error message is displayed, but the
        generation continues.
        """
        if self.config.WIDTH < 9 or self.config.HEIGHT < 7:
            print("Error: Maze too small for '42' pattern. Omitting pattern.")
            self.skip_pattern = True

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

    def _add_loops(self, grid: list[list[int]],
                   ft_pattern: list[list[bool]]) -> None:
        """
        Adds cycles to the maze by removing L extra walls
        between adjacent cells.

        Args:
            grid (list[list[int]]): The maze grid to modify.
            ft_pattern (list[list[bool]]): Matrix where True is a '42' cell.
        """
        L = max(1, int((self.config.WIDTH * self.config.HEIGHT) * 0.02))  # probar y cambiar si hace falta
        extra_corrs = 0
        while extra_corrs < L:
            y = self.rng.randint(0, self.config.HEIGHT - 1)
            x = self.rng.randint(0, self.config.WIDTH - 1)
            if ft_pattern[y][x]:
                continue

            valid_neighbors = []
            for direction, (dy, dx, c_w, n_w) in self.MOVEMENTS.items():
                ny, nx = y + dy, x + dx
                if (0 <= ny < self.config.HEIGHT
                   and 0 <= nx < self.config.WIDTH):
                    if not ft_pattern[ny][nx]:
                        if grid[y][x] & abs(c_w):
                            valid_neighbors.append((ny, nx, c_w, n_w))

            if valid_neighbors:
                ny, nx, c_w, n_w = self.rng.choice(valid_neighbors)
                grid[y][x] += c_w
                grid[ny][nx] += n_w
                extra_corrs += 1

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
        maze_map_str = self._grid_to_hex_str(grid)

        return Maze(
            maze_map=maze_map_str,
            entry=self.config.ENTRY,
            exit=self.config.EXIT
        )


class Algorithms(Enum):
    """A enumerator class for enumarating all possible Algorithms"""
    DEFAULT = ExampleMazeGenerator
    EXAMPLE = ExampleMazeGenerator  # !! BORRAR ANTES DE ENTREGAR
    DFS = DFSMazeGenerator
    pass


class MazeGeneratorFactory(BaseModel):
    """Instance used for creating Maze Generators"""
    @overload
    def create_generator(
        self,
        CONFIG: MazeConfiguration = Field()
    ) -> tuple[MazeGenerator, int]:
        """Creates the appropiate maze generator

        Args:
            config (MazeConfiguration): The MazeConfiguration data-class used
                to create the appropiate maze
        """
        ...

    @overload
    def create_generator(
        self,
        WIDTH: int = Field(),
        HEIGHT: int = Field(),
        ENTRY: tuple[int, int] = Field(),
        EXIT: tuple[int, int] = Field(),
        PERFECT: bool = Field(default=False),
        SEED: float | None = Field(default=None),
        ALGORITHM: str | None = Field(max_length=255, default=None),
        EXTRA: dict[str, str] | None = Field(default=None)
    ) -> tuple[MazeGenerator, int]:
        """Creates the appropiate maze generator

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
            tuple[MazeGenerator, int]: The maze generator and a number
                according to: 0 if the selected algorithm wasn't found or 1 if
                it was found.
        """
        ...

    def create_generator(
        self, *args: Any, **kwargs: Any
    ) -> tuple[MazeGenerator, int]:
        """Creates the appropiate maze generator"""
        if len(args) == 1:
            config = args[0]
        else:
            config = MazeConfiguration(**kwargs)

        for algorithm in Algorithms:
            if algorithm.name == config.ALGORITHM:
                return (algorithm.value(config), 1)
        return (Algorithms.DEFAULT.value(config), 0)
