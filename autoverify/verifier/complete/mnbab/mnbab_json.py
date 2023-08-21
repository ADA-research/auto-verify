"""_sumary_."""
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import IO, Any

from ConfigSpace import Configuration

from autoverify import DEFAULT_VERIFICATION_TIMEOUT_SEC
from autoverify.util.dict import nested_set
from autoverify.util.tempfiles import tmp_file, tmp_json_file_from_dict


class MnbabJsonConfig:
    """Class for mn-bab JSON configs."""

    def __init__(self, json_file: IO[str]):
        """_summary_."""
        self._json_file = json_file

    @classmethod
    def _init_dict_fields(
        cls,
        mnbab_dict: dict[str, Any],
        network: Path,
        property: Path,
        timeout: int,
    ):
        mnbab_dict["network_path"] = str(network)
        mnbab_dict["benchmark_instances_path"] = str(
            cls._temp_instance_file(network, property)
        )
        mnbab_dict["test_data_path"] = str(
            cls._temp_instance_file(network, property)
        )

        mnbab_dict["input_dim"] = [784]  # # TODO: get_input_shape(network)
        mnbab_dict["use_gpu"] = True  # TODO: Make this a choice
        mnbab_dict["bab_batch_sizes"] = [4, 8, 16]  # TODO: Make this a HP?
        mnbab_dict["random_seed"] = 42  # TODO: Param
        mnbab_dict["timeout"] = timeout
        mnbab_dict["experiment_name"] = "mnbab_" + str(datetime.now())
        mnbab_dict["domain_splitting__initial_split_dims"] = [0]  # TODO: HP

        # NOTE: Cant put a boolean in a ConfigSpace Constant???
        mnbab_dict["use_online_logging"] = False

    @classmethod
    def from_json(
        cls,
        json_file: Path,
        network: Path,
        property: Path,
        *,
        timeout: int = DEFAULT_VERIFICATION_TIMEOUT_SEC,
    ):
        """_summary."""
        mnbab_dict: dict[str, Any]

        with open(str(json_file)) as f:
            mnbab_dict = json.load(f)

        cls._init_dict_fields(mnbab_dict, network, property, timeout)

        return cls(tmp_json_file_from_dict(mnbab_dict))

    @classmethod
    def from_config(
        cls,
        config: Configuration,
        network: Path,
        property: Path,
        *,
        timeout: int = DEFAULT_VERIFICATION_TIMEOUT_SEC,
    ):
        """_summary_."""
        dict_config: dict[str, Any] = config.get_dictionary()
        mnbab_dict: dict[str, Any] = {}

        for key, value in dict_config.items():
            nested_keys = key.split("__")
            nested_set(mnbab_dict, nested_keys, value)

        cls._init_dict_fields(mnbab_dict, network, property, timeout)

        return cls(tmp_json_file_from_dict(mnbab_dict))

    def set_timeout(self, timeout: int):
        """_summary_."""
        pass

    def get_json_file(self) -> IO[str]:
        """_summary_."""
        return self._json_file

    def get_json_file_path(self) -> Path:
        """_summary_."""
        return Path(self._json_file.name)

    @staticmethod
    def _temp_instance_file(
        network: Path,
        property: Path,
        *,
        timeout: int = sys.maxsize,
    ) -> Path:
        tmp_csv = tmp_file(".csv")

        with open(tmp_csv.name, "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([str(network), str(property), timeout])

        return Path(tmp_csv.name)
