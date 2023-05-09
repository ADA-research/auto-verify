"""_summary_."""
from ConfigSpace import ConfigurationSpace, Integer

DummyConfigspace = ConfigurationSpace()
DummyConfigspace.add_hyperparameters(
    [
        Integer(
            "temp_int",
            (1, 1000),
            default=64,
        ),
    ]
)
