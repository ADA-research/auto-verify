from dataclasses import dataclass
from pathlib import Path

from autoverify import DEFAULT_VERIFICATION_TIMEOUT_SEC


@dataclass
class VerificationInstance:
    """_summary_."""

    network: Path
    property: Path
    timeout: int

    def as_smac_instance(self) -> str:
        """Return the instance in a `f"{network},{property},{timeout}"` format.

        A SMAC instance has to be passed as a single string to the
        target_function, in which we split the instance string on the comma
        again to obtain the network, property and timeout.

        If no timeout is specified, the `DEFAULT_VERIFICATION_TIMEOUT_SEC`
        global is used.

        Returns:
            str: The smac instance string
        """
        timeout: int = self.timeout or DEFAULT_VERIFICATION_TIMEOUT_SEC

        return f"{str(self.network)},{str(self.property)},{str(timeout)}"

    def as_row(self, resolve_paths: bool = True) -> list[str]:
        """Returns the instance as a list of strings."""
        net = (
            str(self.network.resolve()) if resolve_paths else str(self.network)
        )

        prop = (
            str(self.property.resolve())
            if resolve_paths
            else str(self.property)
        )

        return [net, prop, str(self.timeout)]
