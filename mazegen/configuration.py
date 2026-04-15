from dataclasses import dataclass


@dataclass
class Configuration:
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: str
    ALGORITHM: str
    pass


# TODO
def get_config(file: str = "") -> Configuration: ...
