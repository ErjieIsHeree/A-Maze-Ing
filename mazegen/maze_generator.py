
from dataclasses import dataclass
from abc import ABC, abstractmethod

from .configuration import Configuration


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
        self.config = config
        return

    @abstractmethod
    def generate(self) -> Maze: ...
    ...


# !! BORRAR ANTES DE ENTREGAR
class ExampleMazeGenerator(MazeGenerator):
    def generate(self) -> Maze:
        return Maze("<MAPA_HEXADECIMAL>", "<RUTA>", (0, 0), (19, 24))
    pass


# TODO
class MazeFactory():
    def create_generator(
        self,
        config: Configuration | None = None
    ) -> MazeGenerator:
        ...
    ...
