from dataclasses import dataclass

from ConfigSpace import ConfigurationSpace


@dataclass
class VerifierConfiguration:
    verifier: str
    configuration: ConfigurationSpace
