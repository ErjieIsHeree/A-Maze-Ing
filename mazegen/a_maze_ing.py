
from collections.abc import Callable
import sys

from .configuration import get_config
from .maze_generator import Maze, MazeFactory, MazeGenerator


# TODO
def write_output(maze: Maze) -> None: ...


# TODO
def visualize(generate_maze: Callable) -> None: ...


def create_maze_generator(
    maze_generator: MazeGenerator
) -> Callable:
    def _() -> Maze:
        maze: Maze = maze_generator.generate()
        write_output(maze)
        return maze
    return _


if __name__ == "__main__" and len(sys.argv) == 2:
    maze_generator = MazeFactory().create_generator(get_config(sys.argv[1]))
    visualize(create_maze_generator(maze_generator))
elif __name__ == "__main__":
    print("Please enter only the file name.")
