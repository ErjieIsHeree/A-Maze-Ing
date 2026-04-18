
from abc import ABC, abstractmethod
from enum import Enum
from typing import overload, Self
from pydantic import BaseModel, Field, model_validator, ConfigDict
import sys


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


class Algorithms(Enum):
    """A enumerator class for enumarating all possible Algorithms"""
    DEFAULT = ExampleMazeGenerator
    EXAMPLE = ExampleMazeGenerator  # !! BORRAR ANTES DE ENTREGAR
    pass


class MazeGeneratorFactory():
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

    def create_generator(self, *args, **kwargs) -> tuple[MazeGenerator, int]:
        """Creates the appropiate maze generator"""
        if len(args) == 1:
            config = args[0]
        else:
            config = MazeConfiguration(**kwargs)

        for algorithm in Algorithms:
            if algorithm.name == config.ALGORITHM:
                return (algorithm.value(config), 1)
        return (Algorithms.DEFAULT.value(config), 0)
