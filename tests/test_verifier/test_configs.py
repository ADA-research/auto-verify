import yaml

from autoverify.util.verification_instance import VerificationInstance
from autoverify.verifier.complete.abcrown.abcrown_yaml_config import (
    AbcrownYamlConfig,
)


def test_ab_config_from_yaml(tmp_path, trivial_sat: VerificationInstance):
    yaml_f = tmp_path / "test.yaml"

    with open(yaml_f, "w") as f:
        yaml.dump({"general": {"seed": 42}}, f)

    ab_cfg = AbcrownYamlConfig.from_yaml(
        yaml_f, trivial_sat.network, trivial_sat.property
    )

    with open(ab_cfg.get_yaml_file_path(), "r") as f:
        d = yaml.safe_load(f)
        assert d["general"]["seed"] == 42
