"""VerificationInstance."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from autoverify import DEFAULT_VERIFICATION_TIMEOUT_SEC


@dataclass(frozen=True, eq=True)
class VerificationInstance:
    """VerificationInstance class.

    Attributes:
        network: The `Path` to the network.
        property: The `Path` to the property.
        timeout: Maximum wallclock time.
    """

    network: Path
    property: Path
    timeout: int

    @classmethod
    def from_str(cls, str_instance: str):
        """Create from a comma seperated string."""
        network, property, timeout = str_instance.split(",")
        return cls(Path(network), Path(property), int(timeout))

    def __hash__(self):
        """Hash the VI."""
        return hash(
            (
                self.network.expanduser().resolve(),
                self.property.expanduser().resolve(),
                self.timeout,
            )
        )

    def __str__(self):
        """Short string representation of the `VerificationInstance`."""
        return f"{self.network.name} :: {self.property.name} :: {self.timeout}"

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
            str(self.network.expanduser().resolve())
            if resolve_paths
            else str(self.network)
        )

        prop = (
            str(self.property.expanduser().resolve())
            if resolve_paths
            else str(self.property)
        )

        return [net, prop, str(self.timeout)]

    # HACK: Assuming some names and layouts here...
    def as_simplified_network(self) -> VerificationInstance:
        """changes the network path.

        Assumes a "onnx_simplified" dir is present at the same level.
        """
        simplified_nets_dir = self.network.parent.parent / "onnx_simplified"

        return VerificationInstance(
            simplified_nets_dir / self.network.name, self.property, self.timeout
        )
