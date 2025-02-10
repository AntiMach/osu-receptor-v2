import yaml
from PIL import Image
from pathlib import Path

import osu_receptor.const as const


class Column:
    value: str
    notetail: bool
    color: list[int]
    elements: dict[str, Path]

    def __init__(self, data: dict, token: str) -> None:
        self.value = token
        self.notetail = data["notetail"]
        self.color = data["color"]
        self.elements = {k: Path(data[k].format(token)) for k in const.ELEMENT_MAP}

    def update(self, override: dict):
        self.notetail = override.get("notetail", self.notetail)
        self.color = override.get("color", self.notetail)
        self.elements.update({k: Path(v) for k in const.ELEMENT_MAP if (v := override.get(k))})


class Skin:
    directory: Path
    columns: dict[str, Column]
    images: dict[Path, Image.Image]
    layouts: dict[int, list[Column]]

    def __init__(self, skin_dir) -> None:
        self.directory = Path(skin_dir)

        with (self.directory / const.SKIN_YAML).open("r") as fp:
            data = yaml.load(fp, Loader=yaml.CLoader)

        overrides = data.pop("overrides", {})

        layouts = [str(layout) for layout in data.pop("layouts", [])]
        tokens = {token for layout in layouts for token in layout}
        tokens |= overrides.keys()

        self.columns = {token: Column(data, token) for token in tokens}

        for value, override in overrides.items():
            self.columns[value].update(override)

        self.images = {}
        self.layouts = {len(pattern): [self.columns[token] for token in pattern] for pattern in layouts}

    def __enter__(self):
        try:
            self._open_images()
        except Exception:
            self._close_images()
            raise
        return self

    def __exit__(self, *_):
        self._close_images()

    def _open_images(self):
        for column in self.columns.values():
            for file in column.elements.values():
                self.images[file] = Image.open(self.directory / file)

    def _close_images(self):
        for image in self.images.values():
            image.close()
