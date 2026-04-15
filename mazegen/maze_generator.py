
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum

from .configuration import Configuration


class Algorithms(Enum):
    EXAMPLE = "example"
    pass


@dataclass(frozen=True)
@dataclass
class Maze:
    maze: str
    maze_solution: str
    entry: tuple[int, int]
    exit: tuple[int, int]
    pass


# TODO
class MazeGenerator(ABC):
    def __init__(self, config: Configuration) -> None:
        if not self.is_valid_config(config):
            raise Exception("Not valid config")
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


# TODO
class MazeFactory():
    def create_generator(
        self,
        config: Configuration
    ) -> MazeGenerator:
        match config.ALGORITHM:
            case Algorithms.EXAMPLE:
                maze_generator = ExampleMazeGenerator(config)
            case _:
                raise Exception("Non existing algorithm")
        maze_generator.is_valid_config(config)
        return maze_generator
    ...
