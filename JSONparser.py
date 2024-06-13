import json
from typing import Union
from vector import Vector2  # Assuming you have the Vector2 class from the previous code
from constraints import Constraint, Linear, Radial  # Assuming you have the Constraint, Linear, and Radial classes

class Input:
    def __init__(self, tycon: str, posx: float, posy: float, dir: float = None, mag: float = None):
        self.tycon = tycon
        self.posx = posx
        self.posy = posy
        self.dir = dir
        self.mag = mag

    def __repr__(self):
        return f"Input(tycon={self.tycon}, posx={self.posx}, posy={self.posy}, dir={self.dir}, mag={self.mag})"

def input_to_constraint(input_data: Input) -> Constraint:
    if input_data.tycon == "Linear":
        return Linear(Vector2(input_data.posx, input_data.posy), input_data.dir, input_data.mag)
    elif input_data.tycon == "Radial":
        return Radial(Vector2(input_data.posx, input_data.posy))
    else:
        raise ValueError("Invalid input.")

def from_json(json_str: str) -> Input:
    data = json.loads(json_str)
    return Input(**data)

def to_json(input_data: Input) -> str:
    return json.dumps(input_data.__dict__)
