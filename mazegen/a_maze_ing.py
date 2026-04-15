
from collections.abc import Callable
import sys

from .configuration import get_config
from .maze_generator import Maze, MazeFactory, MazeGenerator


# TODO docstring
def write_output(maze_info: Maze, file: str) -> None:
    try:
        with open(file, "w") as f:
            f.write(maze_info.maze)
            f.write("\n")
            f.write(f"{maze_info.entry[0]}, {maze_info.entry[1]}")
            f.write(f"{maze_info.exit[0]}, {maze_info.exit[1]}")
            f.write(maze_info.maze_solution)
    except Exception as err:
        print(f"[ERROR]: {err}")
    return


# TODO all
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
