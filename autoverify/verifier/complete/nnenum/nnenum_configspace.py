"""_summary_."""
from ConfigSpace import Categorical, ConfigurationSpace

NnenumConfigspace = ConfigurationSpace()
NnenumConfigspace.add_hyperparameters(
    [
        # https://github.com/stanleybak/nnenum/blob/55363ce71bb047f02dec1be0d4d58526c737ff53/src/nnenum/nnenum.py#LL150C25-L150C29
        Categorical(
            "settings_mode",
            ["auto", "control", "image", "exact"],
            default="auto",
        ),
    ]
)
