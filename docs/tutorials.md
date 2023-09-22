# Tutorial

!!! UNDER CONSTRUCTION !!!

!!! UNDER CONSTRUCTION !!!

!!! UNDER CONSTRUCTION !!!

!!! UNDER CONSTRUCTION !!!

!!! UNDER CONSTRUCTION !!!


!!! warning

    Auto-Verify has only been tested for Linux and will not work on MacOS and Windows.

## Getting Started

First of all, make install [Miniconda](TODO LINK). Miniconda is used to manage the environments of different verification tools, other environment managers will _not_ work.

!!! warning

    Anaconda can fail trying to install environments in some cases where Miniconda does not.

After Miniconda is installed, setup Auto-Verify by running the following commands:

```
> conda create -n python=3.10 auto-verify
> conda activate auto-verify
> pip install auto-verify
```

To check if the installation was succesful, run:

```bash
> auto-verify --version
```


## Installing Verifiers

Currently, Auto-Verify supports the following verifiers:

- [nnenum](https://github.com/stanleybak/nnenum) (_Stanley Bak_)
- [AB-Crown](https://github.com/Verified-Intelligence/alpha-beta-CROWN) (_Zhang et al_)
- [VeriNet](https://github.com/vas-group-imperial/VeriNet) (_VAS Group_)
- [Oval-BaB](https://github.com/oval-group/oval-bab) (_OVAL Research Group_)

These verifiers can be installed as follows:

```
> auto-verify install nnenum
> auto-verify install abcrown
> auto-verify install verinet
> auto-verify install ovalbab
```

To uninstall a verifier, run:

```
> auto-verify uninstall [verifier]
```


## Verifying Properties

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

TODO.
