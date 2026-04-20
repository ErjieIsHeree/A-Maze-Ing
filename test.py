from collections.abc import Callable
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
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    pass


def is_closed_wall(map_block: str, wall_side: Wall) -> bool:
    return True if int(map_block, 16) & wall_side.value else False


def write_walls(
    partial_map: str,
    wall_side: Wall,
    path: list[int],
    entry: int | None = None,
    exit: int | None = None
) -> str:
    match wall_side:
        case Wall.SOUTH | Wall.NORTH:
            wall, closed_wall, open_wall = "+", "---+", "   +"
        case Wall.EAST | Wall.WEST:
            wall, closed_wall, open_wall = "|", "   |", "    "
            wall_side = Wall.EAST

    def mark(template: str, char: str) -> str:
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
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)
    pass


def get_new_position(position: tuple[int, int], step: Step) -> tuple[int, int]:
    return (position[0] + step.value[0], position[1] + step.value[1])


def get_path_coordinates(
    paths: list[str],
    entry: tuple[int, int]
) -> set[tuple[int, int]]:
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


if __name__ == "__main__":
    visualize(f)
    pass
