import json
import sys
import svgwriter as SVGWriter
import tensor_field as TF
from constraints import Constraint
from json_parser import from_json, Input, input_to_constraint
from streamline import PlacementMethod, trace_lines
from typing import List
import pathlib

def make_svg(constraints: List[Constraint], fw: float, fh: float, method: PlacementMethod) -> None:
    tf = TF.make_tensor_field(constraints)
    svg_content = SVGWriter.write_svg(
        SVGWriter.append_elements(
            TF.plot_tensor_field(tf, constraints, fw, fh),
            trace_lines(tf, fw, fh, method)
        )
    )
    print(svg_content)

def main() -> None:
    parse_cmd_args(sys.argv[1:])

def parse_cmd_args(args: List[str]) -> None:
    if len(args) == 1 and args[0] == '-h':
        usage()
        sys.exit(0)
    elif len(args) == 1 and args[0] == '-v':
        version()
        sys.exit(0)
    elif len(args) in [3, 4]:
        file, fw, fh = args[:3]
        method = args[3] if len(args) == 4 else 'furthest'
        build_viz(file, float(fw), float(fh), method)
        sys.exit(0)
    else:
        usage()
        sys.exit(1)

def usage() -> None:
    print("usage: tensor <inputFile> <fieldWidth> <fieldHeight> [opt]")

def version() -> None:
    print("Tensor v0.1")

def build_viz(input_file: str, fw: float, fh: float, pmeth: str) -> None:
    input_path = pathlib.Path(input_file)
    if not input_path.is_file():
        print(f"File {input_file} does not exist.")
        sys.exit(1)

    with open(input_file, 'r') as f:
        data = json.load(f)
    
    try:
        inputs = [from_json(json.dumps(item)) for item in data]
    except json.JSONDecodeError as e:
        print(f"Failure on input: {e}")
        sys.exit(1)

    method = {
        "furthest": PlacementMethod.Furthest,
        "random": PlacementMethod.Random,
        "improved": PlacementMethod.Improved
    }.get(pmeth, None)

    if method is None:
        print("Seed placement method not found.")
        sys.exit(1)

    constraints = [input_to_constraint(inp) for inp in inputs]
    make_svg(constraints, fw, fh, method)

if __name__ == "__main__":
    main()
