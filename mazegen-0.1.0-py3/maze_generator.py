
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from typing import overload
import sys

from .configuration import Configuration


@dataclass(frozen=True)
@dataclass
class Maze:
    """Create a data-class with information of a Maze.

    It contains all the information need for the user about the Maze

    Args:
        maze_map: str
        maze_solution: str
        entry: tuple[int, int]
        exit: tuple[int, int]
    """
    maze_map: str
    maze_solutions: list[str] = field(init=False)
    entry: tuple[int, int]
    exit: tuple[int, int]

    def __post_init__(self) -> None:
        """Set the solution to the maze"""
        object.__setattr__(self, "maze_solution", self.__maze_solutioneer())
        return

    def __maze_solutioneer(self) -> list[str]:  # TODO this method
        """Find the different paths to complete de maze.

        Returns:
            list[str]: A list with the solutions of the maze

        Raises:
        """
        return []
    pass


class MazeGenerator(ABC):
    def __init__(self, config: Configuration) -> None:
        self.config = config
        try:
            self.__validate_config()
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
    def __validate_config(self) -> None:
        """Validates if maze can be created with the actual configuration"""
        ...
    pass


class ExampleMazeGenerator(MazeGenerator):  # !! BORRAR ANTES DE ENTREGAR
    def __init__(self, config: Configuration) -> None:
        super().__init__(config)
        return

    def generate(self) -> Maze:
        return Maze("<MAPA_HEXADECIMAL>", (0, 0), (19, 24))

    def __validate_config(self) -> None: ...
    pass


class Algorithms(Enum):
    EXAMPLE = ExampleMazeGenerator  # !! BORRAR ANTES DE ENTREGAR
    pass


class MazeGeneratorFactory():
    """Instance used for creating Maze Generators"""
    @overload
    def create_generator(self, config: Configuration) -> MazeGenerator:
        """Creates the appropiate maze generator

        Args:
            config (Configuration): The configuration data-class used to create
                the appropiate maze
        """
        ...

    @overload
    def create_generator(
        self,
        WIDTH: int,
        HEIGHT: int,
        ENTRY: tuple[int, int],
        EXIT: tuple[int, int],
        OUTPUT_FILE: str,
        PERFECT: bool,
        SEED: float | None,
        ALGORITHM: str,
        EXTRA: dict[str, str] | None
    ) -> MazeGenerator:
        """Creates the appropiate maze generator

        Args:
            WIDTH (int): The width of the maze
            HEIGHT (int): The height of the maze
            ENTRY (tuple[int, int]): The entry point of the maze
            EXIT (tuple[int, int]): The exit point of the maze
            OUTPUT_FILE (str): The width of the maze
            PERFECT (bool): If the maze has only one way to be completed
            SEED (float | None): The seed used to create the maze
            ALGORITHM (str): The algorithm wanted to create the maze
            EXTRA (dict[str, str] | None): Extra data for others special mazes
        """
        ...

    def create_generator(self, *args, **kwargs) -> MazeGenerator:
        """Creates the appropiate maze generator"""
        if len(args) == 1:
            config = args[0]
        else:
            config = Configuration(*args)

        for algorithm in Algorithms:
            if algorithm.__name__ == config.ALGORITHM:
                return algorithm.value(config)
        raise Exception("Non existing algorithm")
