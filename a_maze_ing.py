
from collections.abc import Callable
import sys

from mazegen import MazeGeneratorFactory, MazeGenerator, Maze
from visualizator import visualize
from configuration import get_config


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
            f.write(f"\n{maze_info.entry[0]},{maze_info.entry[1]}")
            f.write(f"\n{maze_info.exit[0]},{maze_info.exit[1]}\n")
            if is_pro:
                text = "\n".join(
                    f"Solution {i}: {solution}"
                    for i, solution in enumerate(maze_info.maze_solutions, 1)
                )
            else:
                text = maze_info.maze_solutions[0]
            f.write(text)
    except Exception as err:
        print(f"[Error]: {err}")
        sys.exit(1)
    return


def create_maze_pipeline(
    maze_generator: MazeGenerator, output_file: str
) -> Callable[[], Maze]:
    """Returns a function to export and get a Maze data-class

    The Maze data-class contains all the information for a user about a maze

    Args:
        maze_generator (MazeGenerator): the maze generator used to generate
            mazes
        output_file (str): the name of the file to export

    Returns:
        Callable[[], Maze]: The function to call
    """
    def _() -> Maze:
        """This function generates, exports and returns a Maze data-class

        Returns:
            Maze: The Maze dataclass with all user information of the maze
        """
        maze: Maze = maze_generator.generate()
        write_output(maze, output_file, False)
        return maze
    return _


if (__name__ == "__main__" and
        len(sys.argv) == 2 or (3 and "--v2" in sys.argv[1:])):
    if len(sys.argv) == 2:
        config = get_config(sys.argv[1])
    else:
        config = get_config(
            sys.argv[2] if sys.argv[1] == "--v2" else sys.argv[1], True)
        pass

    try:
        maze_generator = MazeGeneratorFactory().create_generator(
            **config.model_dump())
    except Exception as err:
        print(f"[ERROR]: {err}")
        sys.exit(1)
    visualize(create_maze_pipeline(maze_generator, config.OUTPUT_FILE))
elif __name__ == "__main__":
    print("""Only 2 arguments are accepted:
-The flag: '--v2'
-A configuration file name""")
