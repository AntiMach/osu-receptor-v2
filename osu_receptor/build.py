import shutil
from pathlib import Path
from io import TextIOWrapper
from typing import Any

import osu_receptor.const as const
from osu_receptor.settings import Settings
from osu_receptor.skin import Skin, Column
from osu_receptor.images import ImageBuilder, make_blank, make_cover


class SkinBuilder:
    in_dir: Path
    out_dir: Path
    asset_dir: Path
    settings: Settings
    skin: Skin
    ini: TextIOWrapper
    images: set[str]

    def __init__(self, path: Path | str) -> None:
        self.in_dir = Path(path)
        self.out_dir = Path(const.BUILD_DIR) / path
        self.asset_dir = self.out_dir / const.ASSET_DIR

        if self.out_dir.exists():
            shutil.rmtree(self.out_dir)

        self.asset_dir.mkdir(parents=True)

        self.settings = Settings(const.SETTINGS_YAML)
        self.skin = Skin(self.in_dir)
        self.ini = (self.out_dir / const.SKIN_INI).open("w", encoding="utf8")

        self.images: set[str] = set()

    def build(self):
        with self.ini, self.skin:
            make_blank().save(self.asset_png(const.BLANK))
            self.images.add(const.BLANK)

            for key_count, pattern in self.skin.layouts.items():
                self.build_key_count(key_count, pattern)

    def write_line(self, s: str = ""):
        return self.ini.write(f"{s}\n")

    def write_header(self, k: int):
        self.write_line("[Mania]")
        self.write_line(f"Keys: {k}")

    def write_entry(self, k: str, v: Any):
        self.write_line(f"{k}: {v}")

    def asset_path(self, name: str) -> Path:
        return self.asset_dir / name

    def asset_png(self, name: str) -> Path:
        return self.asset_path(f"{name}.png")

    def asset_png_2x(self, name: str) -> Path:
        return self.asset_path(f"{name}@2x.png")

    def build_key_count(self, key_count: int, pattern: list[Column]):
        key_settings = self.settings.layouts[key_count]
        self.write_header(key_count)

        self.write_entry("ColumnWidth", ",".join((str(key_settings.fullwidth),) * key_count))
        self.write_entry("HitPosition", const.HEIGHT - key_settings.hitpos)

        if key_settings.centered:
            w, h = key_settings.centered
            self.write_entry(
                "ColumnStart",
                (const.HEIGHT * w / h - key_settings.fullwidth * key_count) / 2,
            )

        if key_settings.cover:
            cover_name = f"cover_{key_count}"
            make_cover(key_settings.fullwidth, key_settings.cover, pattern).save(self.asset_png(cover_name))
            self.images.add(cover_name)

            self.write_entry("StageBottom", self.asset_path(cover_name))

        self.write_line()

        for key, val in key_settings.template.items():
            if val is None:
                val = self.asset_path(const.BLANK)
            self.write_entry(key, val)

        for i, column in enumerate(pattern):
            self.write_line()

            self.write_entry(f"Colour{i + 1}", ",".join(str(c) for c in column.color))

            builder = ImageBuilder(self.skin, column, key_settings)

            for element in const.ELEMENT_MAP:
                if element == const.TAIL and key_settings.is_percy:
                    self.write_entry(
                        const.ELEMENT_MAP[const.TAIL] % i,
                        self.asset_path(const.BLANK),
                    )
                    continue

                full_image_name = builder.full_image_name(element)

                if full_image_name not in self.images:
                    self.images.add(full_image_name)
                    res = builder.make(element)

                    res.save(self.asset_png_2x(full_image_name))
                    res.resize((res.width // 2, res.height // 2)).save(self.asset_png(full_image_name))

                self.write_entry(
                    const.ELEMENT_MAP[element] % i,
                    self.asset_path(full_image_name),
                )

        self.write_line()
        self.write_line()


def build_skin(skin_name: Path | str):
    return SkinBuilder(skin_name).build()
