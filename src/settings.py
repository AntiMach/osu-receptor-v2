import json
import dataclasses
from pathlib import Path

import src.const as const


@dataclasses.dataclass
class Configuration:
    name: str
    width: int
    spacing: int
    hitpos: int
    percy_height: int
    centered: list[int]
    cover: int
    template: dict[str, str]

    @property
    def is_percy(self):
        return self.percy_height > 0

    @property
    def fullwidth(self):
        return self.width + self.spacing * 2

    def override(self, name, data: dict):
        template = data.pop("template", {})
        res = dataclasses.replace(self, name=name, **data)
        res.template = {**res.template, **template}
        return res


class Settings:
    def __init__(self, file_path: str) -> None:
        with Path(file_path).open("r") as fp:
            data = json.load(fp)

        default = Configuration(name=const.DEFAULT, **data.pop(const.DEFAULT))
        names = {const.DEFAULT: default}

        self.configs: dict[int, Configuration] = {
            i: default for i in const.KEYS
        }

        for name, new in data.items():
            key_counts = new.pop("keys")

            for key_count in key_counts:
                newname = f"{self.configs[key_count].name}_{name}"

                self.configs[key_count] = names.setdefault(
                    newname, self.configs[key_count].override(newname, new)
                )
