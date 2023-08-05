

import os
import pathlib
from typing import Optional

import yaml


class DotfileConfig:

    def __init__(self) -> None:
        self.username :Optional[str] = None
        self.password :Optional[str] = None


def load_config() -> Optional[DotfileConfig]:
    dot_path_str = "~/.brownianrc"
    dot_path_str = os.path.expanduser(dot_path_str)
    dot_path = pathlib.Path(dot_path_str)

    if not dot_path.exists():
        return None

    with open(dot_path, "r") as fp:
        dic = yaml.safe_load(fp)

    conf = DotfileConfig()
    conf.username = dic["username"]
    conf.password = dic["password"]
    return conf

    
