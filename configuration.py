import sys
from typing import List, Optional, Dict, Tuple

from pydantic import BaseModel, ConfigDict


class Configuration(BaseModel):
    """Stores the maze generation parameters.

    Attributes:
        WIDTH (int): Maze width in cells.
        HEIGHT (int): Maze height in cells.
        ENTRY (tuple[int, int]): Starting coordinates (x, y).
        EXIT (tuple[int, int]): Ending coordinates (x, y).
        OUTPUT_FILE (str): Path to the resulting maze file.
        PERFECT (bool): Whether the maze is perfect (no loops).
        SEED (Optional[float]): Seed for random number generation.
        ALGORITHM (str): The generation algorithm to use.
        EXTRA (Dict[str, str] | None): Additional non-mandatory parameters.
    """

    model_config = ConfigDict(frozen=True)

    WIDTH: int
    HEIGHT: int
    ENTRY: Tuple[int, int]
    EXIT: Tuple[int, int]
    PERFECT: bool
    SEED: Optional[float]
    ALGORITHM: str
    OUTPUT_FILE: str
    EXTRA: Optional[Dict[str, str]]
    pass


def parse_coords(coords: str, label: str) -> Tuple[int, int]:
    """Parses a string of comma-separated coordinates into a tuple.

    Args:
        coords (str): String in 'x,y' format.

    Returns:
        Tuple[int, int]: A tuple containing the x and y integers.

    Note:
        Exits the program if the format is invalid or values are not integers.
    """

    try:
        clist = coords.split(",")
        if len(clist) != 2:
            raise ValueError()
        return (int(clist[0]), int(clist[1]))
    except ValueError:
        print(f"[ERROR] Invalid syntax in {label}: '{coords}'. Coordinates "
              "must be only two numeric values and follow 'x,y'")
        sys.exit(1)


def parse_bool(txt: str) -> bool:
    """Converts a string to a boolean value.

    Args:
        txt (str): String to convert ('true' or 'false').

    Returns:
        bool: True if txt is 'true', False if 'false'.

    Note:
        Exits the program if the value is not a valid boolean string.
    """

    if txt.lower() == "true":
        return True
    elif txt.lower() == "false":
        return False
    else:
        print(f"Error: Invalid syntax '{txt}'. The 'PERFECT' value must be "
              "a boolean: True or False.")
        sys.exit(1)


def get_val(key: str, data: Dict[str, str], defs: Dict[str, str],
            use_defaults: bool) -> str:
    """Extracts a value from data, removing it, or returns a default.

    Args:
        key (str): The configuration key to look for.
        data (Dict[str, str]): The current configuration dictionary.
        defs (Dict[str, str]): Default values fallback.

    Returns:
        str: The value from data if present and not empty, otherwise default.
    """

    if use_defaults:
        return data.get(key, defs.get(key, ""))
    return data.get(key, "")


def get_config(file: str, use_v2: bool = False) -> Configuration:
    """Reads and validates a configuration file to create a Configuration
    object.

    Args:
        file (str): Path to the config.txt file.

    Returns:
        Configuration: An immutable dataclass with all validated parameters.

    Note:
        Validates mandatory keys, coordinate limits, and positive dimensions.
        Exits the program with a specific error message
        if any validation fails.
    """

    defaults: Dict[str, str] = {
        "WIDTH": "20",
        "HEIGHT": "15",
        "ENTRY": "0,0",
        "EXIT": "19,14",
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": "True",
        "ALGORITHM": "dfs",
        "SEED": "None"
    }
    datadict: Dict[str, str] = {}
    try:
        with open(file, 'r') as f:
            for idl, line in enumerate(f, 1):
                line = line.rstrip('\n')
                if line.startswith('#'):
                    continue
                if not use_v2:
                    if line == "":
                        print(f"[ERROR] (line {idl} in {file}) Empty line.")
                        sys.exit(1)
                    if '=' not in line:
                        print(f"[ERROR] (line {idl} in {file}) Invalid format."
                              " Expected 'KEY=VALUE'.")
                        sys.exit(1)
                    key, value = line.split('=', 1)
                    if key.strip() != key or value.strip() != value:
                        print(f"[ERROR] (line {idl} in {file}) Excess spaces.")
                        sys.exit(1)
                    datadict[key] = value
                else:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        if key.strip() and value.strip():
                            datadict[key.strip()] = value.strip()

    except FileNotFoundError:
        print(f"[ERROR] The file {file} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] (File {file}): {e}")
        sys.exit(1)

    if not use_v2:
        mandatory_keys: List[str] = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                                     "OUTPUT_FILE", "PERFECT"]
        for key in mandatory_keys:
            if key not in datadict.keys():
                print(f"[ERROR] Mandatory key {key} is missing in {file}")
                sys.exit(1)

    try:
        width = int(get_val("WIDTH", datadict, defaults, use_v2))
        height = int(get_val("HEIGHT", datadict, defaults, use_v2))
        entry = parse_coords(get_val("ENTRY", datadict, defaults, use_v2),
                             "ENTRY")
        exit = parse_coords(get_val("EXIT", datadict, defaults, use_v2),
                            "EXIT")
        output_file = get_val("OUTPUT_FILE", datadict, defaults, use_v2)
        perfect = parse_bool(get_val("PERFECT", datadict, defaults, use_v2))
        algorithm = get_val("ALGORITHM", datadict, defaults, use_v2)
        seed_raw = get_val("SEED", datadict, defaults, use_v2)
        seed = float(seed_raw) if seed_raw not in ["None", ""] else None
        extra = datadict if datadict else None

        return Configuration(
            WIDTH=width,
            HEIGHT=height,
            ENTRY=entry,
            EXIT=exit,
            OUTPUT_FILE=output_file,
            PERFECT=perfect,
            SEED=seed,
            ALGORITHM=algorithm,
            EXTRA=extra
        )

    except ValueError as e:
        print(f"[ERROR] (File {file}): {e}")
        sys.exit(1)


if __name__ == "__main__":
    print(get_config(sys.argv[0]))
