"""SDP-CROWN configuration space.

Only supports parameters present in the example YAML:
    - lr_alpha
    - lr_lambda
    - random_seed
    - start
    - end
"""

from ConfigSpace import ConfigurationSpace, Float, Integer

SDPCrownConfigspace = ConfigurationSpace(name="sdpcrown")
SDPCrownConfigspace.add_hyperparameters(
    [
        # SDP-CROWN learning rate for alpha
        Float(
            "lr_alpha",
            (0.01, 1.0),
            default=0.5,
            log=True,
        ),
        # SDP-CROWN learning rate for lambda
        Float(
            "lr_lambda",
            (0.001, 0.1),
            default=0.05,
            log=True,
        ),
    ]
)
