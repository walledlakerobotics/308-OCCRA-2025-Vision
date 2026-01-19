import sys
from typing import Any

import appdirs
import casefy
from pydantic import BaseModel, ConfigDict, field_serializer
from pydantic.alias_generators import to_camel
from pydantic_numpy.typing import Np2DArrayFp64


def convert_case(string: str) -> str:
    match sys.platform:
        case "win32" | "darwin":
            return casefy.titlecase(string)
        case _:
            return casefy.kebabcase(string)


APP_NAME = convert_case("Cube Detector")
APP_AUTHOR = convert_case("308 Monsters")


CONFIG_DIRCTORY = appdirs.user_config_dir(APP_NAME, APP_AUTHOR)

FILE_NAME = "config.json"
# FILE_PATH = os.path.join(CONFIG_DIRCTORY, FILE_NAME)
FILE_PATH = "./config.json"


class Config(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    cameras: dict[str, str] = {
        "main": "\\\\?\\usb#vid_0408&pid_50c5&mi_00#6&26f20a52&0&0000#{e5323777-f976-4f5b-9b55-b94699c46e44}\\global"
    }

    camera_matricies: dict[str, Np2DArrayFp64] = {}
    dist_coeffs: dict[str, Np2DArrayFp64] = {}

    def __init__(self):
        super().__init__()

    def save(self):
        with open(FILE_PATH, "w") as f:
            f.write(self.model_dump_json(indent=4, by_alias=True))

    def __setattr__(self, name: str, value: Any):
        super().__setattr__(name, value)
        self.save()


config = Config()

print(config.model_dump_json(indent=4, by_alias=True))
