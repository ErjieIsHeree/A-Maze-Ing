from collections.abc import Callable
import sys

from .configuration import get_config
from .maze_generator import Maze, MazeFactory, MazeGenerator
from .write_output import write_output
from .visualizator import visualize


def generate_maze(
    maze_generator: MazeGenerator = MazeFactory().create_generator()
) -> Callable:
    def _() -> Maze:
        maze: Maze = maze_generator.generate()
        write_output(maze)
        return maze
    return _


# TODO
def is_valid_txt(file: str) -> bool: ...


if __name__ == "__main__" and len(sys.argv) == 2 and is_valid_txt(sys.argv[1]):
    maze_generator = MazeFactory().create_generator(get_config(sys.argv[1]))
    visualize(generate_maze(maze_generator))
    pass
