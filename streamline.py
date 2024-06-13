import random
from typing import List, Tuple, TypeVar, Generic, Optional
from vector import Vector2
from svgwriter import SVGElem, Polyline
from nearest_neighbour import Storage, NearestNeighbor
import tensor_field as TF
import utils

A = TypeVar('A')

Streamline = List[Vector2]

class PlacementMethod:
    Random = "Random"
    Furthest = "Furthest"
    Improved = "Improved"

def streamline_from_evs(evf: "VectorField", nn: Storage[A], seed: Vector2, fw: float, fh: float) -> Streamline:
    return trace_lines(evf, nn, fw, fh, seed, 0.01, 75)

def draw_streamline(vs: Streamline) -> SVGElem:
    vec_to_pair = lambda v: (v.x, v.y)
    return Polyline(list(map(vec_to_pair, vs)), "green", 0.1)

def random_seeds(n: int, fw: float, fh: float) -> List[Vector2]:
    random.seed(8)
    xs = [random.uniform(0, fw) for _ in range(n)]
    ys = [random.uniform(0, fh) for _ in range(n)]
    return [Vector2(x, y) for x, y in zip(xs, ys)]

def sample_list(xs: List[A]) -> List[A]:
    return xs[::10]

def place_seeds(maj: "VectorField", min: "VectorField", nn: Storage[A], sls: List[Streamline], n: int, fw: float, fh: float) -> Tuple[List[Streamline], Storage[A]]:
    if n == 0:
        return sls, nn

    exist_pts = [p for sl in sls for p in sample_list(sl)]
    trial_pts = random_seeds(10, fw, fh)
    
    def dist(v1: Vector2, v2: Vector2) -> float:
        return (v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2
    
    def closest_pt(v: Vector2) -> float:
        return min(dist(v, pt) for pt in exist_pts) if exist_pts else 2 * fw
    
    seed = utils.argmax(closest_pt, trial_pts)
    maj_sl = streamline_from_evs(maj, nn, seed, fw, fh)
    min_sl = streamline_from_evs(min, nn, seed, fw, fh)
    nn = TF.add_streamline_to_nn(maj_sl, nn)
    nn = TF.add_streamline_to_nn(min_sl, nn)
    
    return place_seeds(maj, min, nn, [maj_sl, min_sl] + sls, n - 1, fw, fh)

def place_seeds_improved(maj: "VectorField", min: "VectorField", nn: Storage[A], sls: List[Streamline], n: int, fw: float, fh: float) -> Tuple[List[Streamline], Storage[A]]:
    if n == 0:
        return sls, nn

    exist_pts = [sample_list(sl) for sl in sls]
    trial_pts = random_seeds(10, fw, fh)
    
    def mk_sls(s: Vector2) -> List[Streamline]:
        return [streamline_from_evs(maj, nn, s, fw, fh), streamline_from_evs(min, nn, s, fw, fh)]
    
    trial_sls = [mk_sls(s) for s in trial_pts]
    sl_sets = [sls + exist_pts for sls in trial_sls]
    
    best_sls = util.argmin(lambda sl_set: chi_squared_even_spacing(fw, fh, 4, sl_set), sl_sets)
    nn = TF.add_streamline_to_nn(best_sls[0], nn)
    
    return place_seeds_improved(maj, min, nn, best_sls, n - 1, fw, fh)

def place_seeds_random(maj: "VectorField", min: "VectorField", nn: Storage[A], sls: List[Streamline], n: int, fw: float, fh: float) -> Tuple[List[Streamline], Storage[A]]:
    if n == 0:
        return sls, nn

    s = random_seeds(1, fw, fh)[0]
    maj_sl = streamline_from_evs(maj, nn, s, fw, fh)
    min_sl = streamline_from_evs(min, nn, s, fw, fh)
    nn = TF.add_streamline_to_nn(maj_sl, nn)
    nn = TF.add_streamline_to_nn(min_sl, nn)
    
    return place_seeds_random(maj, min, nn, [maj_sl, min_sl] + sls, n - 1, fw, fh)

def chi_squared_even_spacing(width: float, height: float, buckets: float, vs: List[List[Vector2]]) -> float:
    def scale(v: Vector2) -> Tuple[int, int]:
        return round(v.x * buckets / width), round(v.y * buckets / width)
    
    bucket_freqs = [len(list(group)) for key, group in groupby(sorted(map(scale, (p for v in vs for p in v))))]
    exp_freq = sum(bucket_freqs) / len(bucket_freqs)
    x2 = [(o - exp_freq) ** 2 / exp_freq for o in bucket_freqs]
    
    return sum(x2)

def place_streamlines(tf: "TensorField", nn: Storage[A], n: int, fw: float, fh: float, method: str) -> List[Streamline]:
    if method == PlacementMethod.Random:
        return place_seeds_random(TF.tensorfield_eigenvectors(tf)[0], TF.tensorfield_eigenvectors(tf)[1], nn, [], n, fw, fh)[0]
    elif method == PlacementMethod.Furthest:
        return place_seeds(TF.tensorfield_eigenvectors(tf)[0], TF.tensorfield_eigenvectors(tf)[1], nn, [], n, fw, fh)[0]
    elif method == PlacementMethod.Improved:
        return place_seeds_improved(TF.tensorfield_eigenvectors(tf)[0], TF.tensorfield_eigenvectors(tf)[1], nn, [], n, fw, fh)[0]
    else:
        raise ValueError("Unknown placement method")

def trace_lines(tf: "TensorField", fw: float, fh: float, method: str) -> List[SVGElem]:
    return [draw_streamline(sl) for sl in place_streamlines(tf, NearestNeighbor(fw, fh, 25).storage, 8, fw, fh, method)]
