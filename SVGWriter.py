import xml.etree.ElementTree as ET
from typing import List, Tuple, Union

# SVG Header as a list of strings
svg_header = [
    '<?xml version="1.0" standalone="no"?>',
    '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"',
    '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
]

class SVGElem:
    pass

class Line(SVGElem):
    def __init__(self, x1: float, y1: float, x2: float, y2: float, color: str, strokewidth: float):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.strokewidth = strokewidth

class Polyline(SVGElem):
    def __init__(self, lines: List[Tuple[float, float]], color: str, strokewidth: float):
        self.lines = lines
        self.color = color
        self.strokewidth = strokewidth

class Rect(SVGElem):
    def __init__(self, x: float, y: float, rwidth: float, rheight: float):
        self.x = x
        self.y = y
        self.rwidth = rwidth
        self.rheight = rheight

class Circle(SVGElem):
    def __init__(self, x: float, y: float, r: float, color: str, strokewidth: float):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.strokewidth = strokewidth

class SVG:
    def __init__(self, width: float, height: float, elems: List[SVGElem]):
        self.width = width
        self.height = height
        self.elems = elems

def self_closing_tag(name: str, attrs: List[Tuple[str, str]]) -> str:
    attr_string = ' '.join([f'{attr}="{value}"' for attr, value in attrs])
    return f'<{name} {attr_string} />'

def append_elements(svg: SVG, new_elems: List[SVGElem]) -> SVG:
    return SVG(svg.width, svg.height, svg.elems + new_elems)

def write_elem(elem: SVGElem) -> str:
    if isinstance(elem, Line):
        attrs = [("x1", str(elem.x1)), ("y1", str(elem.y1)), ("x2", str(elem.x2)), ("y2", str(elem.y2)),
                 ("stroke", elem.color), ("stroke-width", str(elem.strokewidth))]
        return self_closing_tag("line", attrs)
    elif isinstance(elem, Rect):
        attrs = [("x", str(elem.x)), ("y", str(elem.y)), ("width", str(elem.rwidth)), ("height", str(elem.rheight)),
                 ("stroke", "black"), ("stroke-width", "1"), ("fill", "none")]
        return self_closing_tag("rect", attrs)
    elif isinstance(elem, Circle):
        attrs = [("cx", str(elem.x)), ("cy", str(elem.y)), ("r", str(elem.r)),
                 ("stroke", elem.color), ("stroke-width", str(elem.strokewidth)), ("fill", "none")]
        return self_closing_tag("circle", attrs)
    elif isinstance(elem, Polyline):
        points = ' '.join([f'{x},{y}' for x, y in elem.lines])
        attrs = [("points", points), ("stroke", elem.color), ("stroke-width", str(elem.strokewidth)), ("fill", "none")]
        return self_closing_tag("polyline", attrs)
    else:
        raise ValueError("Unknown SVGElem type")

def write_svg(svg: SVG) -> str:
    view = f'0 0 {svg.width} {svg.height}'
    header = [f'<svg width="8cm" height="8cm" viewBox="{view}" xmlns="http://www.w3.org/2000/svg" version="1.1">']
    body = [write_elem(elem) for elem in svg.elems]
    footer = ["</svg>"]
    return '\n'.join(svg_header + header + body + footer)
