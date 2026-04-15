from .configuration import get_config
from .maze_generator import MazeFactory, MazeGenerator
from .maze_solutioner import solutionate
from .send_output import send_output
from .visualizator import visualize
from typing import Generator
import sys
from enum import Enum


class Labels(Enum):
    MAZE = "MAZE"
    SOLUTION = "SOLUTION"
    ENTRY = "ENTRY"
    EXIT = "EXIT"


def generate_maze(
    maze_generator: MazeGenerator = MazeFactory().create_generator()
) -> Generator[dict, None, None]:
    while True:
        maze: str = maze_generator.generate()
        maze_solution: str = solutionate(maze)
        entry: str = maze_generator.get_entry()
        exit: str = maze_generator.get_exit()

        send_output(maze, entry, exit, maze_solution)
        yield {
            Labels.MAZE: maze,
            Labels.SOLUTION: maze_solution,
            Labels.ENTRY: entry,
            Labels.EXIT: exit
        }


if (__name__ == "__main__"
    and len(sys.argv) == 2
        and sys.argv[1] == "config.txt"):
    maze_generator: MazeGenerator = MazeFactory().create_generator(get_config())
    visualize(generate_maze(maze_generator))
    pass
