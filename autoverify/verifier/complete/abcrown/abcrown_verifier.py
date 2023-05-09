"""ab-crown verifier."""
import subprocess
import tempfile
from pathlib import Path

from ConfigSpace import Configuration, ConfigurationSpace
from result import Err, Ok

from autoverify.util import find_substring
from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import cwd
from autoverify.verifier.complete.abcrown.abcrown_configspace import (
    AbCrownConfigspace,
)
from autoverify.verifier.complete.abcrown.abcrown_yaml_config import (
    AbcrownYamlConfig,
)
from autoverify.verifier.verification_result import (
    CompleteVerificationOutcome,
    CompleteVerificationResult,
)
from autoverify.verifier.verifier import CompleteVerifier


class AbCrown(CompleteVerifier):
    """_summary_."""

    name: str = "abcrown"
    config_space: ConfigurationSpace = AbCrownConfigspace

    def _verify_property(
        self,
        network: Path,
        property: Path,
        *,
        config: Configuration | Path | None = None,
    ) -> CompleteVerificationOutcome | Err:
        """_summary_."""
        if isinstance(config, Configuration):
            yaml_config = AbcrownYamlConfig.from_config(
                config, network, property
            ).get_yaml_file()
        elif isinstance(config, Path):
            yaml_config = AbcrownYamlConfig.from_yaml(
                config, network, property
            ).get_yaml_file()
        else:
            raise ValueError("Config should be of type Configuration or Path")

        result_file = Path(tempfile.NamedTemporaryFile("w").name)

        run_cmd = self._get_runner_cmd(Path(yaml_config.name), result_file)

        try:
            with cwd(self.tool_path / "complete_verifier"):
                result = subprocess.run(
                    run_cmd,
                    executable="/bin/bash",
                    capture_output=True,
                    check=True,
                    shell=True,
                )
        except subprocess.CalledProcessError as err:
            print("AbCrown Error:\n")
            print(err.stderr.decode("utf-8"))
            return Err("Exception during call to ab-crown")
        except Exception as err:
            print(f"Exception during call to ab-crown, {str(err)}")
            return Err("Exception during call to ab-crown")

        stdout = result.stdout.decode()
        return self._parse_result(stdout, result_file)

    def _parse_result(
        self,
        tool_result: str,
        result_file: Path,
    ) -> CompleteVerificationOutcome | Err:
        """_summary_."""
        if find_substring("Result: sat", tool_result):
            return CompleteVerificationOutcome("SAT", result_file.read_text())
        elif find_substring("Result: unsat", tool_result):
            return CompleteVerificationOutcome("UNSAT")
        elif find_substring("Result: timeout", tool_result):
            return CompleteVerificationOutcome("TIMEOUT")

        return Err("Failed to determine outcome from result")

    def _get_runner_cmd(self, abcrown_config: Path, result_file: Path) -> str:
        source_cmd = get_conda_source_cmd(get_conda_path())

        return f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        python abcrown.py --config {str(abcrown_config)} \
        --results_file {str(result_file)}
        """
