
from collections.abc import Callable
import sys

from .configuration import get_config
from .maze_generator import Maze, MazeFactory, MazeGenerator


# TODO
def write_output(maze: Maze, file: str) -> None: ...


# TODO
def visualize(generate_maze: Callable) -> None: ...


def create_maze_generator(
    maze_generator: MazeGenerator, output_file: str
) -> Callable:
    def _() -> Maze:
        maze: Maze = maze_generator.generate()
        write_output(maze, output_file)
        return maze
    return _


if __name__ == "__main__" and len(sys.argv) == 2:
    config = get_config(sys.argv[1])
    maze_generator = MazeFactory().create_generator(config)
    visualize(create_maze_generator(maze_generator, config.OUTPUT_FILE))
elif __name__ == "__main__":
    print("Please enter only the file name.")
