"""_summary_."""
from ConfigSpace import ConfigurationSpace, Constant, Integer

MnBabConfigspace = ConfigurationSpace()
MnBabConfigspace.add_hyperparameters(
    [
        Constant(
            "prima_lr",
            0.01,
        ),
    ]
)
