import yaml
from typing import Any
def load_config()->Any:
    with open("src/config.yaml") as f:
        config:Any=yaml.safe_load(f)
    return config