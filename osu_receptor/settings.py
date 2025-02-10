from hashlib import md5
import yaml
from typing import Any
from pathlib import Path
from dataclasses import dataclass, field

import osu_receptor.const as const


@dataclass
class Layout:
    width: int
    spacing: int
    hitpos: int
    centered: tuple[int, int] | None = None
    cover: int | None = None
    percy: int | None = None
    template: dict[str, Any] = field(default_factory=dict)

    @property
    def id(self):
        id_base = (self.width, self.spacing, self.hitpos, self.cover, self.percy)
        return md5(str(id_base).encode()).digest()[:4].hex()

    @property
    def fullwidth(self):
        return self.width + self.spacing * 2

    @property
    def is_percy(self) -> bool:
        return self.percy is not None and self.percy > 0

    def update(self, items: dict[str, Any]):
        self.template.update(items.get("template", {}))

        for k, v in items.items():
            if k != "template":
                setattr(self, k, v)


class Settings:
    layouts: dict[int, Layout]

    def __init__(self, file: Path | str):
        with open(file, "r") as fp:
            default = yaml.load(fp.read(), Loader=yaml.CLoader)

        overrides = default.pop("overrides", [])
        self.layouts = {i: Layout(**default) for i in const.KEYS}

        for override in overrides:
            for key in override.pop("keys"):
                self.layouts[key].update(override)
