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

The structure of the configuration file is a KEY=VALUE file.

### The choosen maze generation algorithm  # TODO for zeta :)

### The reason of the choosen maze generation  # TODO for zeta :)

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
    config: MazeConfiguration("<your params>")
    maze_gen: MazeGenerator = MazeGeneratorFactory().create_generator(config)
    maze: Maze = maze_gen.generate
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
| lduran-f (Luzia) | Algorithm developer |  # TODO ask if zeta wanna add her last name or change roles

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

*Zeta point of view:*  #  TODO for zeta

- **Used tools**

| Tool     | Description              |
| -------- | ------------------------ |
| **No?**  | Used for doing nothing   |
