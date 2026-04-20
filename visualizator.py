from collections.abc import Callable
from enum import Enum
from mazegen import Maze


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


def write_walls(
    partial_map: str,
    wall_side: Wall,
    path: list[int],
    entry: int | None = None,
    exit: int | None = None
) -> str:
    """Returns a string of the walls (closed or open) according to the row of
    the map

    Args:
        partial_map (str): the string representing a row of the maze
        wall_side (Wall): the side of the wall of the row that wants to return
        path (list[int]): the columns that contains part of a path to the exit
        entry (int | None): the entry coordinate if is in the actual row
        exit (int | None): the exit coordinate if is in the actual row
    """
    match wall_side:
        case Wall.SOUTH | Wall.NORTH:
            wall, closed_wall, open_wall = "+", "---+", "   +"
        case Wall.EAST | Wall.WEST:
            wall, closed_wall, open_wall = "|", "   |", "    "
            wall_side = Wall.EAST

    def mark(template: str, char: str) -> str:
        """To print a special case when there is a entry, exit or path mark

        Args:
            template (str): the block space to be changed
            char (str): the mark to add in the block space

        Returns:
            str: The string of the block with the mark
        """
        lst = list(template)
        lst[1] = char
        return "".join(lst)

    for i, block in enumerate(partial_map):
        marker = (
            "X" if i == entry else
            "O" if i == exit else
            "8" if i in path else
            " "
        )
        cw = mark(closed_wall, marker) if marker != " " else closed_wall
        ow = mark(open_wall, marker) if marker != " " else open_wall
        wall += cw if is_closed_wall(block, wall_side) else ow
    return f"{wall}\n"


class Step(Enum):
    """A enumerator indicating the steps to add/remove to go in each
    direction"""
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)
    pass


def get_new_position(position: tuple[int, int], step: Step) -> tuple[int, int]:
    """Gets the new coordinates after the step

    Args:
        position (tuple[int, int]): The actual position to move from
        step (Step): The step to move on

    Returns:
        tuple[int, int]: The new position after the step
    """
    return (position[0] + step.value[0], position[1] + step.value[1])


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
        for step in path:
            step_math = (
                Step.N if step == Step.N.name else
                Step.E if step == Step.E.name else
                Step.S if step == Step.S.name else
                Step.W
            )
            position = get_new_position(position, step_math)
            path_coordinates.add(position)
    return path_coordinates


def write_map(maze: Maze, with_solution: bool) -> str:
    """Returns a visual representation with ASCII chars of the Maze given

    Args:
        maze (Maze): The maze object where info is taken for the creation
        with_solution (bool): If wants to get the maze with the solution

    Returns:
        str: A visual representation of the maze in ASCII"""
    map: str = ""
    path = (
        get_path_coordinates(maze.maze_solutions, maze.entry)
        if with_solution else
        {}
    )
    for i, partial_map in enumerate(maze.maze_map.split("\n")):
        if partial_map:
            if not i:
                map += write_walls(partial_map, Wall.NORTH, [])
            partial_path = (
                [coord[0] for coord in path if coord[1] == i]
                if with_solution else
                []
            )
            entry = maze.entry[0] if maze.entry[1] == i else None
            exit = maze.exit[0] if maze.exit[1] == i else None
            map += write_walls(
                partial_map,
                Wall.EAST,
                partial_path,
                entry, exit
            )
            map += write_walls(partial_map, Wall.SOUTH, [])
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
        maze_map = write_map(maze, with_solution)
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
