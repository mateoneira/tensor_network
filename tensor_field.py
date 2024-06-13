import math
from typing import List, Callable, Tuple, TypeVar
from vector import Vector2, sq_mag
from tensor import Tensor, trivial, from_r_theta, from_xy, scalar_times, eigenvectors, sum_tensors
from constraints import Constraint, Linear, Radial
from svgwriter import SVGElem, Line, Circle, SVG
from nearest_neighbour import Storage, NearestNeighbor
import utils

# Constants
decay_constant = 0.10
cycle_threshold = 0.1
d_sep = 1.0

A = TypeVar('A')

# Drawing Specs

def eigenvector_line(v1: Vector2, v2: Vector2) -> SVGElem:
    return Line(v1.x, v1.y, v2.x, v2.y, "black", 0.05)

def constraint_line(v1: Vector2, v2: Vector2) -> SVGElem:
    return Line(v1.x, v1.y, v2.x, v2.y, "red", 0.1)

def constraint_circle(v: Vector2) -> SVGElem:
    return Circle(v.x, v.y, 0.5, "red", 0.1)

# Data Definition

TensorField = Callable[[Vector2], Tensor]
VectorField = Callable[[Vector2], Vector2]

def make_tensor_field(constraints: List[Constraint]) -> TensorField:
    if not constraints:
        return lambda _: trivial
    def tensor_field(p: Vector2) -> Tensor:
        return sum_tensors([basis_field_at_point(p, c) for c in constraints])
    return tensor_field

def basis_field_at_point(pos: Vector2, constraint: Constraint) -> Tensor:
    k = math.exp(-decay_constant * sq_mag(constraint.posn))
    if constraint.constraint_type == "Linear":
        vector = from_r_theta(constraint.mag, constraint.dir)
    elif constraint.constraint_type == "Radial":
        vector = from_xy(pos.x - constraint.posn.x, pos.y - constraint.posn.y)
    return scalar_times(k, vector)

def tensorfield_eigenvectors(tf: TensorField) -> Tuple[VectorField, VectorField]:
    def tf_ev(p: Vector2) -> Tuple[Vector2, Vector2]:
        return eigenvectors(tf(p))
    return lambda p: tf_ev(p)[0], lambda p: tf_ev(p)[1]

def trace_streamline(vf: VectorField, nn0: Storage[A], w: float, h: float, p0: Vector2, step: float, length: float) -> List[Vector2]:
    def mk_step(ps: List[Vector2], vlast: Vector2, n: int) -> List[Vector2]:
        if n == 0:
            return ps
        if not ps:
            return []

        p = ps[-1]
        dir = vf(p)
        if dir.dot(vlast) <= 0:
            dir = dir.scalar_times(-1)
        cycle = (p.sub(p0).mag() < cycle_threshold) and (length - ((n+10) * step)) > cycle_threshold
        in_bound = p.in_bounds(Vector2(0, 0), Vector2(w, h))
        lookup = NearestNeighbor.lookup(nn0, p)
        i_sect = lookup and (lookup[0].sub(p).mag() < d_sep)
        p_prime = p.add(dir.unit().scalar_times(step))

        if not in_bound:
            return mk_step([p_prime, p] + ps, dir, 0)
        elif i_sect:
            return mk_step([lookup[0], p] + ps, dir, 0)
        else:
            return mk_step([p_prime, p] + ps, dir, n - 1)
        
    def trace_line(dir: float) -> List[Vector2]:
        return mk_step([p0], vf(p0).scalar_times(dir), int(length / step))
    
    return trace_line(1) + trace_line(-1)[::-1]

def add_streamline_to_nn(streamline: List[Vector2], storage: Storage[A]) -> Storage[A]:
    for vector in streamline:
        storage = NearestNeighbor.insert(storage, (vector, 0))
    return storage

def plot_tensor_field(tf: TensorField, constraints: List[Constraint], w: float, h: float) -> SVG:
    sample_pts = [Vector2(vx, vy) for vx in range(1, int(w)+1) for vy in range(1, int(h)+1)]
    major_evs = [tensorfield_eigenvectors(tf)[0](p) for p in sample_pts]
    scaled_major_evs = [v.unit().scalar_times(0.5) for v in major_evs]
    plot_vectors = list(zip(sample_pts, scaled_major_evs))
    
    def mk_vec_line(p_ev: Tuple[Vector2, Vector2]) -> SVGElem:
        p, ev = p_ev
        return eigenvector_line(p, p.add(ev))
    
    def mk_cons(c: Constraint) -> SVGElem:
        if c.constraint_type == "Linear":
            cx = c.mag * math.cos(c.dir)
            cy = c.mag * math.sin(c.dir)
            return constraint_line(c.posn, c.posn.add(Vector2(cx, cy)))
        elif c.constraint_type == "Radial":
            return constraint_circle(c.posn)
    
    return SVG(w, h, [mk_vec_line(p_ev) for p_ev in plot_vectors] + [mk_cons(c) for c in constraints])
