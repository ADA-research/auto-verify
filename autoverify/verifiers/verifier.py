from abc import ABC, abstractmethod
from dataclasses import dataclass

from autoverify.verifiers.types import CompleteVerificationResult, VerifierKind


@dataclass
class Verifier(ABC):
    name: str
    kind: VerifierKind
    config_levels: set[int]

    @abstractmethod
    def verify_property(property, network) -> CompleteVerificationResult:
        pass

    @abstractmethod
    def sample_configuration(config_levels, size):
        pass
