*This project has been created as part of the 42 curriculum by exia, lduran-f.*

# A-MAZE-ING

___

## Description

This project is about making a maze generator module that can be reused and use
it with a main file named 'a_maze_ing.py'. The main file will ask for a
configuration file through arguments while executing the program. It will use
it in order to configure the maze configurations. After a correct set of
configurations, it will show the result though the console like a game and
show some options and of course, an exit option.

___

## Instructions

To start this one is very easy. There is a Makefile with which you will need a
the Makefile package in your computer. But if you are reading this you are
probably a 42 student, don't worry about installing this, I hope you already
know you have it installed.

Now just execute 'make' at the a-maze-ing main root and let it fly.

In case you are a pain in my ass you can proceed by creating the venv or if you
are a monkey just install the requirements directly in your global enviroment.

If you are completly new and want it this way, you can follow the instructions
below:

``` bash
python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install -r requirements.txt

python3 a_maze_ing.py
```

___

## Resources

All the resources used to complete this project.

- [Python docs](https://www.example.com)
- [W3Schools docs](https://www.w3schools.com/)
- [GeeksForGeeks docs](https://www.geeksforgeeks.org/)
- [Claude AI](https://claude.ai/)

___

## Additional sections

Here below will be listed and filled the additional sections required for this
project.

### Structure and format of your config file

The structure of the configuration file is a KEY=VALUE format. Depending on the execution mode, the parser behavior changes:
- Strict Mode (no flag; use_v2=False):
    All mandatory keys must be present, with valid values.
    No empty lines, extra whitespace nor lines not following the format are allowed.
    Commented lines are ignored.
- Flexible Mode (--v2 flag; use_v2=True):
    Spaces, empty lines and lines not following the format are allowed and ignored.
    Default values are used if any key is missing or left empty.

### The chosen maze generation algorithms
**DFS (Depth-First Search) / Recursive Backtracker** and **Growing Tree** are the two algorithms implemented in this project.

The DFS algorithm works by carving paths from a starting cell, always moving to a random unvisited neighbour and pushing it onto a stack. When it reaches a dead end, it backtracks through the stack until it finds a cell with available neighbours, continuing until every cell has been visited.

The Growing Tree algorithm generalises DFS by maintaining an active cell list instead of a strict stack. It alternates between two selection strategies: most of the time it picks the most recently added cell (behaving like DFS), but every 4 steps in the same path it picks a random cell from the active list (behaving like Prim's). This produces a more varied texture while keeping long, winding corridors.

### The reason for the chosen maze generation algorithms
**DFS** was chosen as the primary algorithm for the following reasons:

- It produces **perfect mazes** by construction (DFS on a grid is equivalent to building a spanning tree), satisfying the `PERFECT=True` requirement natively.
- It generates long, winding corridors with few dead ends, making the maze visually appealing and genuinely difficult to solve — unlike Sidewinder or Binary Tree, whose biases are immediately obvious to an evaluator.
- The implementation is simple and robust: an iterative stack avoids Python's recursion limit, and the bitmask wall representation (`N=1, E=2, S=4, W=8`) maps directly to the hexadecimal output format required by the subject.
- Integrating the **42 pattern** is trivial: cells belonging to the pattern are pre-marked as visited before the DFS runs, so the algorithm naturally carves around them without any extra logic.

**Growing Tree** was added as a second algorithm because it **shares ~80% of its code with the DFS implementation** (same grid structure, same wall-removal logic, same "42" pattern handling), so the additional cost was minimal. Its mixed selection strategy produces mazes with a noticeably different texture — slightly more branched and organic — which satisfies intention of supporting multiple generation algorithms while also giving the project more visual variety.

Slower algorithms (Wilson's, Aldous-Broder) were discarded due to their unpredictable runtime on larger grids. Biased algorithms (Binary Tree, Sidewinder) were discarded because their structural patterns are trivially recognisable. Kruskal's and Eller's were discarded because their implementation complexity (Union-Find, per-row set management) offered no advantage over DFS for this project's requirements.

### Reusable parts of the code and how

We can reuse this module, there are 4 mains items for it: MazeGeneratorFactory,
MazeGenerator, Maze and MazeConfiguration.

Follow the next few steps for it:

1. Use the ``MazeGeneratorFactory`` ``create_generator`` static method with the
   ``MazeConfiguration`` class or by introducing the custom parameters manually.
   (All raiseable exceptions occurs at this point)
2. Save the ``MazeGenerator`` returned by the ``create_generator`` method.
3. Call the ``generate`` method from the ``MazeGenerator`` instance any time you want a new maze. (Note that if a seed is set, it will return always the same maze)
4. The returned maze will be in a atributte of the ``Maze`` class. There are 4 datas of the maze:
   - Maze map (maze_map)
   - Entry coordinate (entry)
   - Exit coordinate (exit)
   - Maze solutions (maze_solutions)
Call them each by the name in parenthesis.
5. At the end you will have to figure out how to visualize the maze, good luck :)

Example:

``` python
from mazegen import MazeGeneratorFactory, MazeConfiguration, MazeGenerator, Maze


if __name__ == "__main__":
    config: MazeConfiguration(
        WIDTH=32,
        HEIGHT=32,
        ENTRY=0,0,
        EXIT=0,0,
        PERFECT=False
        SEED=None
        ALGORITHM="dfs"
        EXTRA=None
    )
    maze_gen: MazeGenerator = MazeGeneratorFactory().create_generator(config)
    maze: Maze = maze_gen.generate()
    print(maze.maze_map)
    print(maze.entry)
    print(maze.exit)
    print(maze.maze_solutions)
```

### Team and project management

- **Team and roles**

| Member           | Rol                 |
| ---------------- | ------------------  |
| exia (Erjie Xia) | Project manager     |
| lduran-f (Luzia) | Algorithm developer |

- **Anticipated planning and evolution**

To begin with a global view of the project and each tasks to do was set.

Furthermore, was to convert each tasks into Python signatures (with its
corresponding entry/exit parameters) of course, to do this task a clear view
the needs of each parts is need (which was done in the previous step).

In conclusion, having all little tasks ready will lead us to get a clean work
of developing and testing each tasks sepparately and end with a complete
functional program (If everything was planned and tested correctly).

- **Pros and cons through the development**

*Exia point of view:*
This project organization was exciting, I could release some of the power I got
through the years in programming. Of course, crystal clear, I'm not the best at
it, YET!

My partner did her best at doing her part of the work while adapting to my
structure. Even though I haven't explained it to her!

*Zeta point of view:*
I really enjoyed the algorithm research, understanding and implementation process and all the other tasks I had. This was a very enjoyable project and it was really exciting to see the mazes working!!
Working with Erjie as a team has been great; he was understanding when I had to lower or increase the pace of work; he is extremely organized and was able to visualize the structure of the project before starting it and connected all the puzzle pieces perfectly. I'm proud of our work! :)

- **Used tools**

| Tool     | Description              |
| -------- | ------------------------ |
| **No?**  | Used for doing nothing   |
