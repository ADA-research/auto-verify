"""MNBaB verifier."""

from collections.abc import Iterable
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Any

from ConfigSpace import Configuration, ConfigurationSpace

from autoverify import DEFAULT_VERIFICATION_TIMEOUT_SEC
from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import cwd, environment
from autoverify.verifier.complete.mnbab.mnbab_json import MnbabJsonConfig
from autoverify.verifier.verification_result import CompleteVerificationResult, VerificationResultString
from autoverify.verifier.verifier import CompleteVerifier

from .configspace import MnBabConfigspace


class MnBab(CompleteVerifier):
    """MnBab verifier."""

    name: str = "mnbab"
    config_space: ConfigurationSpace = MnBabConfigspace

    def __init__(self, batch_size: int = 512, cpu_gpu_allocation: tuple[int, int, int] | None = None):
        """Initialize MnBab verifier.

        Args:
            batch_size: Batch size for verification (default: 512)
            cpu_gpu_allocation: CPU/GPU allocation tuple (default: None)
        """
        super().__init__(batch_size=batch_size, cpu_gpu_allocation=cpu_gpu_allocation)

    #
    # def test(self):
    #     """_summary_."""
    #     source_cmd = get_conda_source_cmd(get_conda_path())
    #     env_lib_path = get_conda_path() / "envs" / self.conda_env_name / "lib"
    #
    #     run_cmd = f"""
    #     {" ".join(source_cmd)}
    #     conda activate {self.conda_env_name}
    #     export PYTHONPATH=$PYTHONPATH:$PWD
    #     python src/run_instance.py
    #     """
    #
    #     with cwd(self.tool_path), environment(
    #         LD_LIBRARY_PATH=str(env_lib_path)
    #     ):
    #         subprocess.run(run_cmd, executable="/bin/bash", shell=True)
    #
    @property
    def contexts(self) -> list[AbstractContextManager[None]]:
        env_lib_path = get_conda_path() / "envs" / self.conda_env_name / "lib"

        return [
            cwd(self.tool_path),
            environment(LD_LIBRARY_PATH=str(env_lib_path)),
        ]

    def _parse_result(
        self,
        output: str,
        result_file: Path | None,
    ) -> tuple[VerificationResultString, str | None]:
        """Parse the verification result.

        Args:
            output: Command output
            result_file: Path to result file

        Returns:
            Tuple of (result, counter_example)
        """
        # TODO: Implement proper result parsing based on mnbab output
        # For now, return a basic implementation
        if result_file and result_file.exists():
            try:
                with open(result_file) as f:
                    result_content = f.read()
                    if "SAT" in result_content:
                        return "SAT", result_content
                    elif "UNSAT" in result_content:
                        return "UNSAT", None
                    elif "TIMEOUT" in result_content:
                        return "TIMEOUT", None
            except Exception:
                pass

        # Fallback parsing from output
        if "SAT" in output:
            return "SAT", output
        elif "UNSAT" in output:
            return "UNSAT", None
        elif "TIMEOUT" in output:
            return "TIMEOUT", None

        # Default to timeout if we can't parse
        return "TIMEOUT", None

    def _get_run_cmd(
        self,
        network: Path,
        property: Path,
        *,
        config: Path,
        timeout: int = DEFAULT_VERIFICATION_TIMEOUT_SEC,
    ) -> tuple[str, Path | None]:
        from autoverify.util.tempfiles import tmp_file

        with tmp_file(".txt") as tmp:
            result_file = Path(tmp.name)

        source_cmd = get_conda_source_cmd(get_conda_path())

        run_cmd = f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        export PYTHONPATH=$PYTHONPATH:$PWD
        python src/utilities/prepare_instance.py \\
        -b mnbabtest \\
        -n {str(network)} \\
        -s {str(property)} \\
        -r {str(result_file)} \\
        -t {timeout}
        """

        return run_cmd, result_file

    def _init_config(
        self,
        network: Path,
        property: Path,
        config: Configuration | Path,
        *,
        batch_size: int | None = None,
    ) -> Path:
        if isinstance(config, Configuration):
            json_config = MnbabJsonConfig.from_config(config, network, property)
        elif isinstance(config, Path):
            json_config = MnbabJsonConfig.from_json(config, network, property)
        else:
            raise ValueError("Config should be a Configuration, Path or None")

        return Path(json_config.get_json_file_path())

    def _verify_batch(
        self,
        instances: Iterable[Any],
        *,
        config: Configuration | Path | None,
    ) -> list[CompleteVerificationResult]:
        """Verify a batch of instances.

        Args:
            instances: Iterable of verification instances
            config: Configuration to use for verification

        Returns:
            List of verification results
        """
        # TODO: Implement batch verification for mnbab
        # For now, verify instances one by one
        results = []
        for instance in instances:
            result = self.verify_instance(instance, config=config)
            results.append(result)
        return results

    @staticmethod
    def is_same_config(config1: Configuration | str, config2: Configuration | str) -> bool:
        """Check if two configurations are the same.

        Args:
            config1: First configuration
            config2: Second configuration

        Returns:
            True if configurations are the same, False otherwise
        """
        # TODO: Implement proper configuration comparison for mnbab
        # For now, convert to strings and compare
        return str(config1) == str(config2)
