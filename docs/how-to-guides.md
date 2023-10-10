# How-To-Guides

## Verifying Properties

### Simple Example

After installing one or more verifiers, here is how to use them to verify a property. Networks should be in the [ONNX](https://github.com/onnx/onnx) format, properties in the [VNNLIB](https://www.vnnlib.org/) format.

```py
from pathlib import Path
from result import Err, Ok
from autoverify.verifier import AbCrown

if __name__ == "__main__":
    verifier = AbCrown()

    network = Path("my_network.onnx")
    prop = Path("my_property.vnnlib")

    result = verifier.verify_property(network, prop)

    if isinstance(result, Ok):
        outcome = result.unwrap().result
        print("Verification finished, result:", outcome)
    elif isinstance(result, Err):
        print("Error during verification:")
        print(result.unwrap_err().stdout)
```

### Running VNNCOMP Benchmarks

Auto-Verify supports reading benchmarks defined in VNNCOMP style, which are benchmarks with the following structure:

```
vnncomp2022
└── test_props
    ├── instances.csv
    ├── onnx
    │   ├── test_nano.onnx
    │   ├── test_sat.onnx
    │   └── test_unsat.onnx
    └── vnnlib
        ├── test_nano.vnnlib
        └── test_prop.vnnlib
```

Where `instances.csv` is a `csv` file with 3 columns: network, property, timeout. For example, the `test_props` directory contains the following 3 verification instaces:

```
onnx/test_sat.onnx,vnnlib/test_prop.vnnlib,60
onnx/test_unsat.onnx,vnnlib/test_prop.vnnlib,60
onnx/test_nano.onnx,vnnlib/test_nano.vnnlib,60
```

VNNCOMP Benchmarks can found at the following links: [2022](https://github.com/ChristopherBrix/vnncomp2022_benchmarks/tree/main/benchmarks), [2023](https://github.com/ChristopherBrix/vnncomp2023_benchmarks/tree/main/benchmarks). Make sure to unzip all files inside the benchmark after you have downloaded it.

Below is a code snippet that runs this benchmark. Note the `Path` pointing to the benchmark location.

```py
from pathlib import Path

from result import Err, Ok

from autoverify.util.instances import read_vnncomp_instances
from autoverify.verifier import Nnenum

test_props = read_vnncomp_instances(
    "test_props", vnncomp_path=Path("../benchmark/vnncomp2022")
)

if __name__ == "__main__":
    verifier = Nnenum()

    for instance in test_props:
        print(instance)
        result = verifier.verify_instance(instance)

        if isinstance(result, Ok):
            outcome = result.unwrap().result
            print("Verification finished, result:", outcome)
        elif isinstance(result, Err):
            print("Error during verification:")
            print(result.unwrap_err().stdout)
```

## Parallel Portfolios

TODO.
