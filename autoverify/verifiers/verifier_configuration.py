import json
from dataclasses import dataclass

from ConfigSpace import ConfigurationSpace
from ConfigSpace.read_and_write import json as cs_json


@dataclass
class VerifierConfiguration:
    verifier: str
    configuration: ConfigurationSpace

    def write_to_json(self, file_name: str):
        cs_string = cs_json.write(self.configuration)

        json_configuration = json.loads(cs_string)
        json_configuration["verifier"] = self.verifier

        with open(file_name + ".json", "w") as f:
            f.write(json.dumps(json_configuration, indent=2))

    def load_from_json(self, file_name: str):
        with open(file_name, "r") as f:
            json_configuration = json.load(f)

        self.verifier = json_configuration["verifier"]
        json_configuration["verifier"] = None
        self.configuration = cs_json.read(json.dumps(json_configuration))
