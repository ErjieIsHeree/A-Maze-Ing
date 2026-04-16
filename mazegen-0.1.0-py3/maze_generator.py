
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum
from typing import overload

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
    maze_solutions: list[str]
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
        """
        return []
    pass


# TODO all
class MazeGenerator(ABC):
    @overload
    def __init__(self, config: Configuration): ...

    @overload
    def __init__(
        self,
        WIDTH: int,
        HEIGHT: int,
        ENTRY: tuple[int, int],
        EXIT: tuple[int, int],
        OUTPUT_FILE: str,
        PERFECT: bool,
        SEED: float,
        ALGORITHM: str,
        EXTRA: dict[str, str] | None
    ): ...

    def __init__(self, *args, **kwargs) -> None:
        if len(args) == 1:
            config = args[0]
        else:
            config = Configuration(*args)

        if not self.is_valid_config(config):
            raise Exception(f"[Error in {__file__}]")
        self.config = config
        return

    @abstractmethod
    def generate(self) -> Maze: ...

    @abstractmethod
    def is_valid_config(self, config: Configuration) -> bool: ...
    pass


# !! BORRAR ANTES DE ENTREGAR
class ExampleMazeGenerator(MazeGenerator):
    def __init__(self, config: Configuration) -> None:
        super().__init__(config)
        return

    def generate(self) -> Maze:
        self.is_valid_config(self.config)
        return Maze("<MAPA_HEXADECIMAL>", "<RUTA>", (0, 0), (19, 24))

    def is_valid_config(self, config: Configuration) -> bool: ...
    pass


# TODO think if there is a way to dynamize the selection of
class Algorithms(Enum):
    EXAMPLE = "example"
    pass


# TODO all
class MazeFactory():
    def create_generator(
        self,
        config: Configuration
    ) -> MazeGenerator:
        match config.ALGORITHM:
            case Algorithms.EXAMPLE:  # !! Borrar antes de entregar
                maze_generator = ExampleMazeGenerator(config)  # !! Borrar antes de entregar
            case _:
                raise Exception("Non existing algorithm")
        maze_generator.is_valid_config(config)
        return maze_generator
    ...
