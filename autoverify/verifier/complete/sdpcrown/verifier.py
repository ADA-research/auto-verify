"""SDP-CROWN verifier."""

from collections.abc import Iterable
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Any

from ConfigSpace import Configuration, ConfigurationSpace

from autoverify import DEFAULT_VERIFICATION_TIMEOUT_SEC
from autoverify.util import find_substring
from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import cwd, pkill_matches
from autoverify.util.path import check_file_extension
from autoverify.util.tempfiles import tmp_file
from autoverify.verifier.complete.sdpcrown.configspace import SDPCrownConfigspace
from autoverify.verifier.complete.sdpcrown.sdpcrown_yaml_config import SDPCrownYamlConfig
from autoverify.verifier.verification_result import (
    CompleteVerificationResult,
    VerificationResultString,
)
from autoverify.verifier.verifier import CompleteVerifier


class SDPCrown(CompleteVerifier):
    """SDP-CROWN."""

    name: str = "sdpcrown"
    config_space: ConfigurationSpace = SDPCrownConfigspace

    def __init__(
        self,
        batch_size: int = 512,
        cpu_gpu_allocation: tuple[int, int, int] | None = None,
        yaml_override: dict[str, Any] | None = None,
    ):
        """Init SDPCrown verifier."""
        if cpu_gpu_allocation and cpu_gpu_allocation[2] < 0:
            raise ValueError("SDP-CROWN CPU only mode not yet supported")

        super().__init__(batch_size, cpu_gpu_allocation)
        self._yaml_override = yaml_override

    # Override the default ONNX-only check from CompleteVerifier so that
    # SDP-CROWN can also be used with PyTorch `.pth` checkpoints. We still
    # enforce that the network file exists, and that the property is a
    # valid `.vnnlib` file.
    @staticmethod
    def _check_instance(network: Path, property: Path) -> None:
        """Check that the network/property files exist and have supported formats.

        SDP-CROWN supports:
        - Networks saved as ONNX (`.onnx`) for the original workflow.
        - Networks saved as PyTorch checkpoints (`.pth`), which are then
          loaded by `sdp_crown.py --model <path>` (used in the VERONA
          integration for adversarial-training-box models).
        """
        if not network.is_file():
            raise FileNotFoundError(f"Network {network} does not exist.")
        if network.suffix not in {".onnx", ".pth"}:
            raise ValueError("Network should be in onnx or pth format")

        if not check_file_extension(property, ".vnnlib"):
            raise ValueError("Property should be in vnnlib format")

    @property
    def contexts(self) -> list[AbstractContextManager[None]]:
        return [
            cwd(self.tool_path),
            pkill_matches(["python sdp_crown.py"]),
        ]

    def _parse_result(
        self,
        output: str,
        result_file: Path | None,
    ) -> tuple[VerificationResultString, str | None]:
        if find_substring("Result: sat", output):
            if result_file and result_file.exists():
                with open(str(result_file)) as f:
                    counter_example = f.read()

            else:
                # SDP-CROWN with compute_bounds only gives existence, not a specific
                # adversarial input, hence counter_example will always be None
                counter_example = None

            return "SAT", counter_example
        elif find_substring("Result: unsat", output):
            return "UNSAT", None
        elif find_substring("Result: timeout", output):
            return "TIMEOUT", None

        return "TIMEOUT", None

    def _get_run_cmd(
        self,
        network: Path,
        property: Path,
        *,
        config: Path,
        timeout: int = DEFAULT_VERIFICATION_TIMEOUT_SEC,
    ) -> tuple[str, Path | None]:
        with tmp_file(".txt") as tmp:
            result_file = Path(tmp.name)
        source_cmd = get_conda_source_cmd(get_conda_path())

        # Build the command to run SDP-CROWN for a single instance.
        # Note: We do not forward the timeout here; auto-verify enforces the
        # overall timeout at the process level in `_run_verification`.
        run_cmd = f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python sdp_crown.py \
            --model {str(network)} \
            --config {str(config)} \
            --vnnlib_property {str(property)}
        """

        return run_cmd, result_file

    #
    def _verify_batch(
        self,
        instances: Iterable[Any],
        *,
        config: Configuration | Path | None,
    ) -> list[CompleteVerificationResult]:
        """Batch verification not supported yet."""
        raise NotImplementedError("Batch verification not supported for SDP-CROWN.")

    def _init_config(
        self,
        network: Path,
        property: Path,
        config: Configuration | Path,
    ) -> Path:
        if isinstance(config, Configuration):
            yaml_config = SDPCrownYamlConfig.from_config(
                config,
                yaml_override=self._yaml_override,
            )
        else:  # isinstance(config, Path)
            yaml_config = SDPCrownYamlConfig.from_yaml(
                config,
                yaml_override=self._yaml_override,
            )

        return Path(yaml_config.get_yaml_file_path())
