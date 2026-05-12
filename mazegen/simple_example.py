from maze_generator import MazeGeneratorFactory, MazeConfiguration, MazeGenerator, Maze


if __name__ == "__main__":
    """Here is a little example of how to use the maze generator;
    
    1.Use the MazeConfiguration class to set a class of configurations for
    the MazeGenerator class
    
    2.Use the create_generator() function of the MazeGeneratorFactory class and
    send the previous created MazeConfiguration or you can send the explicitly.
    This will return a MazeGenerator class

    3.Use the generate() function to generate Maze classes
    
    4.Read the Maze class attributes (maze_map, entry, exit, maze_solutions) to
    get the maze specifications.
    
    ----------------------------------Maze map---------------------------------
    The maze_map is a long string of hexagesimal numbers. Each representing a
    little block of the map, by converting them into binaries values you can
    decipher the map:
        0000 -> No wall is closed
        0001 -> West wall is open
        0010 -> South wall is open
        0100 -> East wall is open
        1000 -> North wall is open

    Having this in mind, you can have for sure that all blocks are coordinated
    so that you don't have anomallies like having the left block with the east
    wall open and the right block with the west wall closed.
    
    The entry and the exit both are a tuple of [int, int] simulating a (x,y)
    coordinate, (from 0 to width - 1 or height - 1) (width is the x and height
    the y).
    
    The maze solutions contains a list of the multiple paths that can be
    followed from the entry to the exit. The parths are in NSWE convention:
        N -> One step to the North
        S -> One step to the South
        W -> One step to the West
        E -> One step to the East

    -------------------------------Notes---------------------------------------
    1 - Mutliple maze solution is only avaiable below with a map of an area
    smaller than 32x32
    2 - Exit and entry must be within maze bounds (x in (0 -> width - 1) and
    y in (0 -> height - 1))
    3 - There is a pattern 42 in the maze with closed walls, if the entry or
    exit is set inside it, it will exit with an error
    4 - Please just dont do extreme cases, use ur brain and PLEASE, don't make
    enormous mazes or your pc could explode.
    5 - EXTRA param was made for others algorithms that need more data. For now
    it is uselss.
    
    -------------------------------Raises--------------------------------------
    ValueError if ALGORITHM sent doesn't exist.

    """
    config: MazeConfiguration = MazeConfiguration(
        WIDTH=32,
        HEIGHT=32,
        ENTRY=(0,0),
        EXIT=(31,31),
        PERFECT=True
    )
    maze_gen: MazeGenerator = MazeGeneratorFactory().create_generator(config)
    maze: Maze = maze_gen.generate()
    print(maze.maze_map)
    print(maze.entry)
    print(maze.exit)
    print(maze.maze_solutions)
