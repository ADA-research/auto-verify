"""Usage: python gen_inst_csv.py <target_dir>

Creates an `instances.csv` file linking each network to each property.
"""

import csv
import sys
from pathlib import Path

file_path = Path(__file__)
target_dir = file_path.parent / Path(sys.argv[1])
TIMEOUT = 60

if __name__ == "__main__":
    nets, props = [], []

    # Split path so we have relative path from instances.csv pov
    for onnx_path in (target_dir / "onnx").rglob("*.onnx"):
        nets.append(Path(*onnx_path.parts[-2:]))

    for vnnlib_path in (target_dir / "vnnlib").rglob("*.vnnlib"):
        props.append(Path(*vnnlib_path.parts[-2:]))

    inst_file = target_dir / "instances.csv"

    with open(str(inst_file), "w") as f:
        writer = csv.writer(f)
        for net in nets:
            for prop in props:
                writer.writerow([str(net), str(prop), str(TIMEOUT)])
