import json
from pathlib import Path
from PIL import Image

import src.const as const


class Column:
    notetail: bool
    color: list[int]
    elements: dict[str, str]

    def __init__(self, data) -> None:
        self.notetail = data.pop("notetail")
        self.color = data.pop("color")
        self.elements = {k: data[k] for k in const.ELEMENT_MAP}

    def override(self, data):
        data = {
            "notetail": self.notetail,
            "color": self.color,
            **self.elements,
            **data,
        }
        return self.__class__(data)


class Source:
    def __init__(self, skin_dir) -> None:
        self.directory = Path(skin_dir)

        with (self.directory / const.SKIN_JSON).open("r") as fp:
            skin_data = json.load(fp)

        skin_columns = skin_data["columns"]
        skin_layouts = skin_data["layouts"]

        self.default = Column(skin_columns.pop(const.DEFAULT))
        self.columns: dict[str, Column] = {
            name: self.default.override(data)
            for name, data in skin_columns.items()
        }

        self.images: dict[str, Image.Image] = {}
        self.layouts: dict[int, list[Column]] = {
            len(pattern): [
                self.columns.get(token, self.default) for token in pattern
            ]
            for pattern in skin_layouts
        }

        self.register_images(self.default)
        for token in self.columns.values():
            self.register_images(token)

    def register_images(self, column: Column):
        for name in column.elements.values():
            self.images[name] = None

    def open_images(self):
        try:
            self.images = {
                name: Image.open(self.directory / f"{name}.png")
                for name in self.images
            }
        except Exception:
            self.close_images()
            raise

    def close_images(self):
        for image in self.images.values():
            if image is not None:
                image.close()

    def __enter__(self):
        self.open_images()
        return self

    def __exit__(self, *_):
        self.close_images()
