from vector import Vector2  

class Constraint:
    def __init__(self, constraint_type: str, posn: Vector2, dir: float = None, mag: float = None):
        self.constraint_type = constraint_type
        self.posn = posn
        self.dir = dir
        self.mag = mag

    def __repr__(self):
        if self.constraint_type == 'Linear':
            return f"Linear(posn={self.posn}, dir={self.dir}, mag={self.mag})"
        elif self.constraint_type == 'Radial':
            return f"Radial(posn={self.posn})"
        else:
            return "Unknown Constraint"

def Linear(posn: Vector2, dir: float, mag: float) -> Constraint:
    return Constraint('Linear', posn, dir, mag)

def Radial(posn: Vector2) -> Constraint:
    return Constraint('Radial', posn)
