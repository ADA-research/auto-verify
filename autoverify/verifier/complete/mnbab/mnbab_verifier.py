"""Nnenum verifier."""
# TODO: More links and details in above docstring
import os
import subprocess
from pathlib import Path

from ConfigSpace import Configuration, ConfigurationSpace
from result import Err

from autoverify.util import find_substring
from autoverify.util.conda import get_conda_path, get_conda_source_cmd
from autoverify.util.env import cwd, environment, sys_path
from autoverify.verifier.complete.mnbab.mnbab_json import MnbabJsonConfig
from autoverify.verifier.verification_result import CompleteVerificationOutcome
from autoverify.verifier.verifier import CompleteVerifier

from .mnbab_configspace import MnBabConfigspace


class MnBab(CompleteVerifier):
    """_summary_."""

    name: str = "mnbab"
    config_space: ConfigurationSpace = MnBabConfigspace

    def _verify_property(
        self,
        network: Path,
        property: Path,
        *,
        config: Configuration | Path | None = None,
    ) -> CompleteVerificationOutcome | Err[str]:
        """_summary_."""
        if isinstance(config, Configuration):
            json_config = MnbabJsonConfig.from_config(config, network, property)
        elif isinstance(config, Path):
            json_config = MnbabJsonConfig.from_json(config, network, property)
        else:
            raise ValueError("Config should be a Configuration, Path or None")

        json_config = json_config.get_json_file()
        run_cmd = self._get_runner_cmd(Path(json_config.name))

        try:
            with cwd(self.tool_path):
                result = subprocess.run(
                    run_cmd,
                    executable="/bin/bash",
                    capture_output=False,
                    check=True,
                    shell=True,
                )
        except subprocess.CalledProcessError as err:
            print("MnBaB Error:\n")
            print(err.stderr.decode("utf-8"))
            return Err("Exception during call to mn-bab")
        except Exception as err:
            print(f"Exception during call to mn-bab, {str(err)}")
            return Err("Exception during call to mn-bab")

        stdout = result.stdout.decode()
        # print("=" * 80)
        # print(stdout)
        # print("=" * 80)
        return 0  # self._parse_result(stdout)  # TODO:

    def _get_runner_cmd(self, mnbab_config: Path) -> str:
        source_cmd = get_conda_source_cmd(get_conda_path())

        return f"""
        {" ".join(source_cmd)}
        conda activate {self.conda_env_name}
        export PYTHONPATH=$PYTHONPATH:$PWD
        python src/verify.py -c {str(mnbab_config)}
        """
