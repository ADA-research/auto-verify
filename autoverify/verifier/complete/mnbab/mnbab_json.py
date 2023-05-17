"""_sumary_."""
import csv
import json
import sys
from pathlib import Path
from typing import IO, Any

from ConfigSpace import Configuration

from autoverify.util.dict import nested_set
from autoverify.util.tempfiles import tmp_file, tmp_json_file_from_dict


class MnbabJsonConfig:
    """Class for mn-bab JSON configs."""

    def __init__(self, json_file: IO[str]):
        """_summary_."""
        self._json_file = json_file

    @classmethod
    def from_json(cls, json_file: Path, network: Path, property: Path):
        """_summary."""
        mnbab_dict: dict[str, Any]

        with open(str(json_file)) as f:
            mnbab_dict = json.load(f)

        mnbab_dict["network_path"] = str(network)
        mnbab_dict["benchmark_instances_path"] = str(
            cls._temp_instance_file(network, property)
        )

        return cls(tmp_json_file_from_dict(mnbab_dict))

    @classmethod
    def from_config(cls, config: Configuration, network: Path, property: Path):
        """_summary_."""
        dict_config: dict[str, Any] = config.get_dictionary()
        mnbab_dict: dict[str, Any] = {}

        for key, value in dict_config.items():
            nested_keys = key.split("__")
            nested_set(mnbab_dict, nested_keys, value)

        mnbab_dict["network_path"] = str(network)
        mnbab_dict["benchmark_instances_path"] = str(
            cls._temp_instance_file(network, property)
        )

        return cls(tmp_json_file_from_dict(mnbab_dict))

    def get_json_file(self) -> IO[str]:
        """_summary_."""
        return self._json_file

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
