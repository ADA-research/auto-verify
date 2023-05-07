"""_summary_."""
from ConfigSpace import ConfigurationSpace, Integer

OvalBabConfigspace = ConfigurationSpace()
OvalBabConfigspace.add_hyperparameters(
    [
        Integer(
            "temp_int",
            (1, 1000),
            default=64,
        ),
    ]
)
