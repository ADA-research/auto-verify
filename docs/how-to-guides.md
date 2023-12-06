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

## Algorithm Configuration

Each of the verification tools comes equipped with a [`ConfigurationSpace`](https://github.com/automl/ConfigSpace), which can be used to sample Configuration for a verification tool. For example:

```py
from autoverify.verifier import Nnenum

if __name__ == "__main__":
    verifier = Nnenum()
    config = verifier.config_space.sample_configuration()
    print(config)
```

### SMAC Example

We can apply algorithm configuration techniques (or hyperparameter optimization) using [SMAC](https://github.com/automl/SMAC3). In the example below, we try to find a configuration for AB-CROWN on the first 10 instances of the `mnist_fc` benchmark from VNNCOMP2022.

```py
import sys
from pathlib import Path

from ConfigSpace import Configuration
from result import Err, Ok
from smac import AlgorithmConfigurationFacade, Scenario

from autoverify.util.instances import (
    read_vnncomp_instances,
    verification_instances_to_smac_instances,
)
from autoverify.util.smac import index_features
from autoverify.util.verification_instance import VerificationInstance
from autoverify.verifier import AbCrown

mnist = read_vnncomp_instances("mnist_fc", vnncomp_path=Path("../benchmark/vnncomp2022"))[:10]
verifier = AbCrown()

def target_function(config: Configuration, instance: str, seed: int):
    seed += 1  # Mute unused var warnings; (cant rename to _)
    verif_inst = VerificationInstance.from_str(instance)
    result = verifier.verify_instance(verif_inst, config=config)

    # SMAC handles exception by setting cost to `inf`
    verification_result = result.unwrap_or_raise(Exception)
    return float(verification_result.took)

if __name__ == "__main__":
    cfg_space = verifier.config_space
    name = verifier.name
    instances = verification_instances_to_smac_instances(mnist)

    scenario = Scenario(
        cfg_space,
        name="ab_tune",
        instances=instances,
        instance_features=index_features(instances),
        walltime_limit=600,
        output_directory=Path("ab_tune_out"),
        n_trials=sys.maxsize,  # Using walltime limit instead
    )

    smac = AlgorithmConfigurationFacade(
        scenario, target_function, overwrite=True
    )

    inc = smac.optimize()
    print(inc)
```

For more examples on how to use SMAC, please refer to the [SMAC documentation](https://automl.github.io/SMAC3/main/).

### Parallel Portfolios

!!! note

    Custom verification tools are not yet supported for parallel portfolios.

#### Constructiong a Portfolio

Portfolios can be constructed as shown below. In this example, we try construct a portfolio using the `Hydra` algorithm on the `mnist_fc` benchmark from VNNCOMP2022. We include four verification tools that are able to be included and give the procedure a walltime limit of 24 hours.

```py
from pathlib import Path

from autoverify.portfolio import Hydra, PortfolioScenario
from autoverify.util.instances import read_vnncomp_instances

benchmark = read_vnncomp_instances("mnist_fc", vnncomp_path=Path("../benchmark/vnncomp2022"))

if __name__ == "__main__":
    pf_scenario = PortfolioScenario(
        ["nnenum", "abcrown", "ovalbab", "verinet"],
        [
            ("nnenum", 0, 0),
            ("verinet", 0, 1),
            ("abcrown", 0, 1),
            ("ovalbab", 0, 1),
        ],
        benchmark,
        4,
        (60 * 60 * 24) / 4,
        alpha=0.9,
        output_dir=Path("PF_mnist_fc"),
    )

    hydra = Hydra(pf_scenario)
    pf = hydra.tune_portfolio()
    pf.to_json(Path("mnist_fc_portfolio.json"))
```

Portfolios can be manually created as shown below. This example creates a portfolio of 2 verifiers (nnenum and AB-Crown), where nnenum is given 4 CPU cores and 0 GPUs and AB-Crown is given 4 cores and 1 GPU.

```py
from autoverify.portfolio.portfolio import ConfiguredVerifier, Portfolio
from autoverify.util.verifiers import get_verifier_configspace

if __name__ == "__main__":
    pf = Portfolio(
        ConfiguredVerifier(
            "nnenum",
            get_verifier_configspace("nnenum").sample_configuration(),
            (4, 0),
        ),
        ConfiguredVerifier(
            "abcrown",
            get_verifier_configspace("abcrown").get_default_configuration(),
            (4, 1),
        ),
    )

    print(pf)
```

#### Running a Portfolio

Portfolios can be read from a `json` or by specifying the verification tools in Python code. Below is an example of how to run a portfolio in parallel on some instances. Lets take the portfolio we created in the previous example and run it on the same benchmark.

```py
from pathlib import Path

from autoverify.portfolio import Portfolio, PortfolioRunner
from autoverify.util.instances import read_vnncomp_instances


benchmark = read_vnncomp_instances("mnist_fc", vnncomp_path=Path("../benchmark/vnncomp2022"))

if __name__ == "__main__":
    mnist_pf = Portfolio.from_json(Path("mnist_fc_portfolio.json"))
    pf_runner = PortfolioRunner(mnist_pf)

    pf_runner.verify_instances(
        benchmark,
        out_csv=Path("PF_mnist_fc_results.csv"),
    )
```
