from collections.abc import Callable
from typing import Optional
from enum import Enum
import random

from pydantic import BaseModel, Field

from mazegen import Maze


class MapVisuals(BaseModel):
    """This class is used as a data-class containing information of the way
    a map is visualized

    Args:
        corner (str): The char used for corners
        h_wall (str): The char used for horizontal walls
        v_wall (str): The char used for vertical walls
        entry_c (str): The char used for entry point
        exit_c (str): The char used for exit point
        path_c (str): The char used for solution paths
        corner (str): The char used for corners
    """
    corner: str = Field(min_length=1, max_length=1, default="+")
    h_wall: str = Field(min_length=3, max_length=3, default="---")
    v_wall: str = Field(min_length=1, max_length=1, default="|")

    entry_c: str = Field(min_length=1, max_length=1, default="X")
    exit_c: str = Field(min_length=1, max_length=1, default="O")
    path_c: str = Field(min_length=1, max_length=1, default="8")
    pass


def create_maze_row(
    partial_map: str,
    path: list[int],
    map_visual: MapVisuals,
    entry: int | None = None,
    exit: int | None = None,
    with_roof: bool = False
) -> str:
    """Returns a string of the horizontal and south walls of the partial_map

    Args:
        partial_map (str): the string representing a row of the maze
        path (list[int]): the columns that are part of the rout to the exit of
            the maze
        entry (int | None): the column entry point of the maze if it is in the
            actual row
        exit (int | None): the column exit point of the maze if it is in the
            actual row
        with_roof (bool): if want to write the NORTH wall of the actual row,
            default value is False

    Returns:
        A string "picture" of the actual row
    """

    class Wall(Enum):
        """A enumerator class for identifying walls.

        Each binary of a 4 bits sequence (0000) represents a wall. Being it in the
        corresponding order West - South - East - North. So that a 1 means close
        and a 0 means opens.

        Accordingly with that, the next numbers represents that only that wall is
        closed:
            North = 1 (0001)
            EAST =  2 (0010)
            SOUTH = 4 (0100)
            WEST =  8 (1000)
        So that this class contains the wall closed
        """
        NORTH = 1
        EAST = 2
        SOUTH = 4
        WEST = 8
        pass
    def is_closed_wall(map_block: str, wall_side: Wall) -> bool:
        """This function indentify if a wall of a block is closed

        Args:
            map_block (str): A single character representating a block of the maze
            wall_side (Wall): The wall side that want to check

        Returns:
            bool: If the checked wall of the block is open or closed
        """
        return True if int(map_block, 16) & wall_side.value else False
    wall = (
        ("".join(
            f"{map_visual.corner}{map_visual.h_wall}"
            for _ in partial_map
        ) + "+\n") if with_roof else ""
    )

    wall += map_visual.v_wall
    for i, block in enumerate(partial_map):
        marker = (
            map_visual.entry_c if i == entry else
            map_visual.exit_c if i == exit else
            map_visual.path_c if i in path else
            " "
        )
        cw = (f" {marker} " + map_visual.v_wall if block != "F" else
              "###" + map_visual.v_wall)
        ow = f" {marker}  "
        wall += cw if is_closed_wall(block, Wall.EAST) else ow
    wall += "\n"

    wall += map_visual.corner
    for block in partial_map:
        wall += (
            map_visual.h_wall + map_visual.corner
            if is_closed_wall(block, Wall.SOUTH) else
            "   " + map_visual.corner
        )
    return f"{wall}\n"


def write_map(
    maze: Maze,
    map_visual: MapVisuals = MapVisuals(),
    with_solution: bool = False,
    with_solutions: bool = False
) -> str:
    """Returns a visual representation with ASCII chars of the Maze given

    Args:
        maze (Maze): The maze object where info is taken for the creation
        map_visual (MapVisuals): The data-class used to write the maze with its
            characters. By default, the default characters of the MapVisuals
            will be used
        with_solution (bool): If wants to get the maze with the shortest
            solution, by default this is False
        with_solutions (bool): If wants to get the maze with all solutions,
            note that if this is on, with_solution parameter will be skipped.
            By default this is False

    Returns:
        str: A visual representation of the maze in ASCII characters
    """
    
    def get_path_coordinates(
        paths: list[str],
        entry: tuple[int, int]
    ) -> set[tuple[int, int]]:
        """Convert the paths into coordinates of the maze. (No duplicated)

        Args:
            paths (list[str]): A list with all the paths to the exit
            entry (tuple[int, int]): The entry coordinate

        Returns:
            set[tuple[int, int]]: A set of the coordinates to the exit
        """

        class Step(Enum):
            """A enumerator indicating the steps to add/remove to go in each
            direction"""
            N = (0, -1)
            E = (1, 0)
            S = (0, 1)
            W = (-1, 0)
            pass
        position: tuple[int, int] = entry
        path_coordinates: set[tuple[int, int]] = {(entry)}

        for path in paths:
            for step_dir in path:
                step = (
                    Step.N if step_dir == Step.N.name else
                    Step.E if step_dir == Step.E.name else
                    Step.S if step_dir == Step.S.name else
                    Step.W
                )
                position = position[0] + step.value[0], position[1] + step.value[1]
                path_coordinates.add(position)
            position = entry
        return path_coordinates
    map: str = ""
    paths_coordinates: set[tuple[int, int]] = (
        get_path_coordinates(
            (maze.maze_solutions if with_solutions else
             [min(maze.maze_solutions, key=len)]),
            maze.entry
        )
        if with_solution or with_solutions else
        set()
    )

    for i, partial_map in enumerate(maze.maze_map.split("\n")):
        if partial_map:
            partial_path = [coord[0] for coord in paths_coordinates
                            if coord[1] == i]
            entry = maze.entry[0] if maze.entry[1] == i else None
            exit = maze.exit[0] if maze.exit[1] == i else None

            map += create_maze_row(
                partial_map,
                partial_path,
                map_visual,
                entry,
                exit,
                i == 0
            )
    return map


def visualize(
    generate_maze: Callable[[], Maze]
) -> None:
    """Starts an interactive menu to play with mazes.

    It will offer differents options:
        1 - Re-generate the maze
        2 - Show/Hide the shortest path to the exit
        3 - Change wall colours
        4 - Show/Hide every path to the exit
        5 - Change Maze visuals
        6 - Exit

    Each one doing its corresponding action.

    Args:
        generate_maze (Callable): A function that generates Maze objects
    """
    def get_maze_map_visual() -> MapVisuals:
        """Creates a MazeVisuals class asking the user for the chars to use.

        Returns:
            MapVisuals a data-class of chars used to visualize a Map"""
        while True:
            print("\033[u\033[J\n", end="")
            try:
                return MapVisuals(
                    corner=input("Entry corner char (only 1): "),
                    v_wall=input("Entry vertical wall char (only 1): "),
                    h_wall=input("Entry horizontal wall char (only 3): "),
                    entry_c=input("Entry entry char (only 1): "),
                    exit_c=input("Entry exit char (only 1): "),
                    path_c=input("Entry path char (only 1): ")
                )
            except Exception as err:
                print(f"[ERROR]: {err}")
                input("Press enter to continue...")
    colors: list[str] = [
        "\033[30m",
        "\033[31m",
        "\033[32m",
        "\033[33m",
        "\033[34m",
        "\033[35m",
        "\033[36m",
        "\033[37m",
        "\033[90m",
        "\033[91m",
        "\033[92m",
        "\033[93m",
        "\033[94m",
        "\033[95m",
        "\033[96m",
        "\033[97m",
        "\033[1;30m",
        "\033[1;31m",
        "\033[1;32m",
        "\033[1;33m",
        "\033[1;34m",
        "\033[1;35m",
        "\033[1;36m",
        "\033[1;37m",
        "\033[38;5;1m",
        "\033[38;5;2m",
        "\033[38;5;3m",
        "\033[38;5;4m",
        "\033[38;5;5m",
        "\033[38;5;6m",
        "\033[38;5;7m",
        "\033[38;5;9m",
        "\033[38;5;10m",
        "\033[38;5;11m",
        "\033[38;5;12m",
        "\033[38;5;13m",
        "\033[38;5;14m",
        "\033[38;5;15m",
        "\033[38;5;21m",
        "\033[38;5;27m",
        "\033[38;5;33m",
        "\033[38;5;39m",
        "\033[38;5;45m",
        "\033[38;5;51m",
        "\033[38;5;46m",
        "\033[38;5;47m",
        "\033[38;5;48m",
        "\033[38;5;82m",
        "\033[38;5;118m",
        "\033[38;5;154m",
        "\033[38;5;190m",
        "\033[38;5;226m",
        "\033[38;5;220m",
        "\033[38;5;214m",
        "\033[38;5;208m",
        "\033[38;5;202m",
        "\033[38;5;196m",
        "\033[38;5;197m",
        "\033[38;5;198m",
        "\033[38;5;199m",
        "\033[38;5;200m",
        "\033[38;5;201m",
        "\033[38;5;165m",
        "\033[38;5;129m",
        "\033[38;5;93m",
        "\033[38;5;57m",
        "\033[38;5;21m",
        "\033[38;5;20m",
        "\033[38;5;19m",
        "\033[38;5;18m",
        "\033[38;5;17m",
        "\033[38;5;16m",
        "\033[38;5;231m",
        "\033[38;5;230m",
        "\033[38;5;229m",
        "\033[38;5;228m",
        "\033[38;5;227m",
        "\033[38;5;123m",
        "\033[38;5;122m",
        "\033[38;5;121m",
        "\033[38;5;120m",
        "\033[38;5;119m",
        "\033[38;5;87m",
        "\033[38;5;86m",
        "\033[38;5;85m",
        "\033[38;5;84m",
        "\033[38;5;83m",
        "\033[38;5;75m",
        "\033[38;5;74m",
        "\033[38;5;73m",
        "\033[38;5;72m",
        "\033[38;5;71m",
        "\033[38;5;105m",
        "\033[38;5;106m",
        "\033[38;5;107m",
        "\033[38;5;108m",
        "\033[38;5;109m",
        "\033[38;5;177m",
        "\033[38;5;178m",
        "\033[38;5;179m",
        "\033[38;5;180m"
    ]
    selection: int = 0
    maze: Maze = generate_maze()
    with_solution: bool = False
    with_solutions: bool = False
    invalid_input: bool = False
    maze_map_visual: MapVisuals = MapVisuals()
    color: str = ""

    print("\033[s")
    while selection != 6:
        print("\033[u\033[J\n", end="")
        print(
            f"Please enter a valid number (1-6)\n" if invalid_input else
            (f"{color}{write_map(maze, maze_map_visual, with_solution, with_solutions)}\033[0m")
        )
        invalid_input = False
        try:
            selection = int(input(f"""Please insert a number from 1-6:
1 - Re-generate the maze
2 - Show/Hide the shortest path to the exit
3 - Change wall colours
4 - Show/Hide every path to the exit
5 - Change Maze visuals
6 - Exit\n"""))
        except ValueError:
            invalid_input = True
        match selection:
            case 1:
                maze, with_solution, with_solutions = (
                    generate_maze(), False, False)
            case 2:
                with_solution, with_solutions = not with_solution, False
            case 3:
                color = random.choice(colors)
            case 4:
                with_solution, with_solutions = False, not with_solutions
            case 5:
                maze_map_visual = get_maze_map_visual()
            case 7:
                pass
            case _:
                invalid_input = True
    return


if __name__ == "__main__":
    def f() -> Maze:
        """A function used for quick testing the visualize function

        Returns:
            Maze: A maze object."""
        return Maze(
            maze_map="""9515391539551795151151153
EBABAE812853C1412BA812812
96A8416A84545412AC4282C2A
C3A83816A9393584453A82D02
96842A852AC07AAD13A8283C2
C1296C43AAB83AA92AA8686BA
92E853968428444682AC12902
AC3814452FA83FFF82C52C42A
85684117AFC6857FAC1383D06
C53AD043AFFFAFFF856AA8143
91441294297FAFD501142C6BA
AA912AC3843FAFFF82856D52A
842A8692A92B8517C4451552A
816AC384468285293917A9542
C416928513C443A828456C3BA
91416AA92C393A82801553AAA
A81292AA814682C6A8693C6AA
A8442C6C2C1168552C16A9542
86956951692C1455416928552
C545545456C54555545444556""",
            entry=(1, 1),
            exit=(19, 14),
            maze_solutions=["NWES"]
        )

    visualize(f)
    pass
