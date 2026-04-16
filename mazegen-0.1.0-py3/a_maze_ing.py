
from collections.abc import Callable
import sys

from .configuration import get_config
from .maze_generator import Maze, MazeFactory, MazeGenerator


def write_output(maze_info: Maze, file: str, is_pro: bool = False) -> None:
    """Write maze data to a file.

    Writes the maze map, entry and exit coordinates, and solution
    to the specified file. Prints an error message if the operation fails.

    Args:
        maze_info (Maze): Object containing the maze map, entry/exit points,
            and solution.
        file (str): Path to the output file.
    """
    try:
        with open(file, "w") as f:
            f.write(maze_info.maze_map)
            f.write("\n")
            f.write(f"{maze_info.entry[0]}, {maze_info.entry[1]}")
            f.write(f"{maze_info.exit[0]}, {maze_info.exit[1]}")
            if is_pro:
                text = "\n".join(
                    f"Solution {i}: {solution}"
                    for i, solution in enumerate(maze_info.maze_solutions, 1)
                )
            else:
                text = maze_info.maze_solutions[0]
            f.write(text)
    except Exception as err:
        print(f"""[Error in: {__file__} at line {sys._getframe().f_lineno}]:
    {err}""")
        sys.exit(1)
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
