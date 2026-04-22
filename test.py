from collections.abc import Callable
from pydantic import BaseModel, Field
from enum import Enum


class Maze():
    maze_map: str = "9515391539551795151151153\nEBABAE812853C1412BA812812\n96A8416A84545412AC4282C2A\nC3A83816A9395384453A82D02\n96842A852AC07AAD13A8283C2\nC1296C43AAB83AA92AA8686BA\n92E853968428444682AC12902\nAC3814452FA83FFF82C52C42A\n85684117AFC6857FAC1383D06\nC53AD043AFFFAFFF856AA8143\n91441294297FAFD501142C6BA\nAA912AC3843FAFFF82856D52A\n842A8692A92B8517C4451552A\n816AC384468285293917A9542\nC416928513C443A828456C3BA\n91416AA92C393A82801553AAA\nA81292AA814682C6A8693C6AA\nA8442C6C2C1168552C16A9542\n86956951692C1455416928552\nC545545456C54555545444556\n"
    entry: tuple[int, int] = (1, 1)
    exit: tuple[int, int] = (19, 14)
    maze_solutions: list[str] = ["SWSESWSESWSSSEESEEENEESESEESSSEEESSSEEENNENEE"]
    pass


def f() -> Maze:
    return Maze()


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


class MapVisuals(BaseModel):
    corner: str = Field(min_length=1, max_length=1, default="+")
    v_wall: str = Field(min_length=3, max_length=3, default="---")
    h_wall: str = Field(min_length=1, max_length=1, default="|")

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
    is_first: bool = False
) -> str:
    """Returns a string of the horizontal and south walls of the partial_map

    Args:
        partial_map (str): the string representing a row of the maze
        path (list[int]): the columns that contains part of a path to the exit
        entry (int | None): the entry coordinate if is in the actual row
        exit (int | None): the exit coordinate if is in the actual row
    """

    wall = (
        ("".join(
            f"{map_visual.corner}{map_visual.v_wall}"
            for _ in partial_map
        ) + "+\n") if is_first else ""
    )

    wall += map_visual.h_wall
    for i, block in enumerate(partial_map):
        marker = (
            map_visual.entry_c if i == entry else
            map_visual.exit_c if i == exit else
            map_visual.path_c if i in path else
            " "
        )
        cw = f" {marker} " + map_visual.h_wall
        ow = f" {marker}  "
        wall += cw if is_closed_wall(block, Wall.EAST) else ow
    wall += "\n"

    wall += map_visual.corner
    for block in partial_map:
        wall += (
            map_visual.v_wall + map_visual.corner
            if is_closed_wall(block, Wall.SOUTH) else
            "   " + map_visual.corner
        )
    return f"{wall}\n"


class Step(Enum):
    """A enumerator indicating the steps to add/remove to go in each
    direction"""
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)
    pass


def get_path_coordinates(
    paths: list[str],
    entry: tuple[int, int]
) -> set[tuple[int, int]]:
    """Convert the paths into coordinates of the maze. (No duplicated)

    Args:
        paths (list[str]): A list with all the paths to the exit
        entry (tuple[int, int]): The entry coordinate

    Returns:
        set[tuple[int, int]]: A set of the coordinates that is used by the path
            to exit
    """
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
    return path_coordinates


def write_map(maze: Maze, with_solution: bool, map_visual: MapVisuals) -> str:
    """Returns a visual representation with ASCII chars of the Maze given

    Args:
        maze (Maze): The maze object where info is taken for the creation
        with_solution (bool): If wants to get the maze with the solution

    Returns:
        str: A visual representation of the maze in ASCII
    """
    map: str = ""
    path = (
        get_path_coordinates(maze.maze_solutions, maze.entry)
        if with_solution else
        {}
    )
    for i, partial_map in enumerate(maze.maze_map.split("\n")):
        if partial_map:
            partial_path = (
                [coord[0] for coord in path if coord[1] == i]
                if with_solution else
                []
            )
            entry = maze.entry[0] if maze.entry[1] == i else None
            exit = maze.exit[0] if maze.exit[1] == i else None

            map += create_maze_row(
                partial_map,
                partial_path,
                map_visual,
                entry,
                exit,
                True if i == 0 else False
            )
    return map


def visualize(generate_maze: Callable[[], Maze]) -> None:
    """Use mlx to visualize a Maze object

    Args:
        generate_maze (Callable): A function that generates Maze objects

    Returns:
        None
    """

    opt: str = "1-3"
    selection: int = 0
    maze: Maze
    with_solution: bool = False
    invalid_input: bool = False

    print("\033[s")
    maze = generate_maze()
    while selection != 4:
        print("\033[u\033[J", end="")
        maze_map = write_map(maze, with_solution, MapVisuals())
        print(
            maze_map if not invalid_input else
            f"Please enter a valid number ({opt})\n"
        )
        invalid_input = False
        try:
            selection = int(input(f"""Please insert a number from {opt}:
1 - Re-generate the maze
2 - Show/Hide the shortest path to the exit
3 - Change wall colours
4 - Exit\n"""))
        except ValueError:
            invalid_input = True
        match selection:
            case 1:
                maze = generate_maze()
                with_solution = False
            case 2:
                with_solution = not with_solution
            case 3:
                print("Color changed")
            case 4:
                pass
            case _:
                invalid_input = True
    return


if __name__ == "__main__":
    visualize(f)
