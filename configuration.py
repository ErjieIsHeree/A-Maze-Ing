import sys
from typing import List, Optional, Dict

from pydantic import BaseModel, ConfigDict


class Configuration(BaseModel):
    model_config = ConfigDict(frozen=True)

    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    PERFECT: bool
    SEED: Optional[float]
    ALGORITHM: str
    OUTPUT_FILE: str
    EXTRA: Dict[str, str] | None
    pass


def parse_coords(coords: str) -> tuple:
    try:
        clist = coords.split(",")
        if len(clist) != 2:
            raise ValueError()
        nlist = []
        for c in clist:
            nlist.append(int(c))
        return tuple(nlist)
    except ValueError:
        print(f"Error: Invalid syntax: {coords}. Coordinates must be "
              "only two numeric values and follow 'x,y'")
        sys.exit(1)


def parse_bool(txt: str) -> bool:
    if txt.lower() == "true":
        return True
    elif txt.lower() == "false":
        return False
    else:
        print(f"Error: Invalid syntax '{txt}'. The 'PERFECT' value must be "
              "a boolean: True or False.")
        sys.exit(1)


def get_val(key: str, data: dict[str, str], defs: dict[str, str]) -> str:
    val = data.pop(key, "")
    if val == "":
        return defs.get(key)
    return val


def get_config(file: str) -> Configuration:
    defaults: Dict[str, str] = {
        "WIDTH": "20",
        "HEIGHT": "15",
        "ENTRY": "0,0",
        "EXIT": "19,14",
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": "True",  # TODO hablar con zeta que cuando falten config basicos debe lanzar exception. sorry zeta
        "ALGORITHM": "dfs",   # cuidado caso perfect definido false pero algoritmo no definido
        "SEED": "None"
    }
    datadict: Dict[str, str] = {}
    try:
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    if key:
                        datadict[key] = value.strip()
    except FileNotFoundError:
        print(f"Error: The file {file} was not found.")
        sys.exit(1)

    mandatory_keys: List[str] = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                                 "OUTPUT_FILE", "PERFECT"]
    for key in mandatory_keys:
        if key not in datadict.keys():
            print(f"Error: Mandatory key {key} is missing in {file}")
            sys.exit(1)

    try:
        width = int(get_val("WIDTH", datadict, defaults))
        height = int(get_val("HEIGHT", datadict, defaults))
        entry = parse_coords(get_val("ENTRY", datadict, defaults))
        exit = parse_coords(get_val("EXIT", datadict, defaults))
        output_file = get_val("OUTPUT_FILE", datadict, defaults)
        perfect = parse_bool(get_val("PERFECT", datadict, defaults))
        algorithm = get_val("ALGORITHM", datadict, defaults)
        seed_raw = get_val("SEED", datadict, defaults)
        seed = float(seed_raw) if seed_raw != "None" else None

        if width <= 0 or height <= 0:
            raise ValueError("WIDTH and HEIGHT must be positive integers.")

        if entry == exit:
            raise ValueError("ENTRY and EXIT must be different coordinates.")

        for (x, y) in [entry, exit]:
            if not (0 <= x < width and 0 <= y < height):
                raise ValueError(f"ENTRY and EXIT must be coordinates inside"
                                 f" the grid limits ({width}x{height})")  # actual limits (-1)?

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
        print(f"Error found in configuration file {file}: {e}")
        sys.exit(1)
