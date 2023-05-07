import shutil
from pathlib import Path

import src.const as const
from src.settings import Settings
from src.source import Source, Column
from src.images import ImageBuilder, make_blank, make_cover


class SkinBuilder:
    def __init__(self, name) -> None:
        self.in_dir = Path(const.SOURCE_DIR) / name
        self.out_dir = Path(const.BUILD_DIR) / name
        self.asset_dir = self.out_dir / const.ASSET_DIR

        if self.out_dir.exists():
            shutil.rmtree(self.out_dir)

        self.asset_dir.mkdir(parents=True)

        self.settings = Settings(const.SETTINGS_JSON)
        self.skin = Source(self.in_dir)
        self.ini = (self.out_dir / const.SKIN_INI).open("w", encoding="utf8")

        self.images: set[str] = set()

    def write_line(self, s: str = ""):
        return self.ini.write(f"{s}\n")

    def write_header(self, k: int):
        self.write_line("[Mania]")
        self.write_line(f"Keys: {k}")

    def write_entry(self, k, v):
        self.write_line(f"{k}: {v}")

    def ini_path(self, name):
        return f"{const.ASSET_DIR}/{name}"

    def asset_path(self, name):
        return self.asset_dir / f"{name}.png"

    def asset_path_2x(self, name):
        return self.asset_dir / f"{name}@2x.png"

    def build(self):
        with self.ini, self.skin:
            make_blank().save(self.asset_path(const.BLANK))
            self.images.add(const.BLANK)

            for key_count, pattern in self.skin.layouts.items():
                self.build_key_count(key_count, pattern)

    def build_key_count(self, key_count: int, pattern: list[Column]):
        key_settings = self.settings.configs[key_count]
        self.write_header(key_count)

        self.write_entry(
            "ColumnWidth", ",".join((str(key_settings.fullwidth),) * key_count)
        )
        self.write_entry("HitPosition", const.HEIGHT - key_settings.hitpos)

        if key_settings.centered:
            w, h = key_settings.centered
            self.write_entry(
                "ColumnStart",
                (const.HEIGHT * w / h - key_settings.fullwidth * key_count) / 2,
            )

        if key_settings.cover:
            cover_name = f"cover_{key_count}"
            make_cover(
                key_settings.fullwidth, key_settings.cover, pattern
            ).save(self.asset_path(cover_name))

            self.images.add(cover_name)
            self.write_entry("StageBottom", self.ini_path(cover_name))

        self.write_line()

        for key, val in key_settings.template.items():
            if val is None:
                val = self.ini_path(const.BLANK)
            self.write_entry(key, val)

        for i, token in enumerate(pattern):
            self.write_line()

            self.write_entry(
                f"Colour{i+1}", ",".join(str(c) for c in token.color)
            )

            builder = ImageBuilder(self.skin, token, key_settings)

            for element in const.ELEMENT_MAP:
                if element == const.TAIL and key_settings.is_percy:
                    self.write_entry(
                        const.ELEMENT_MAP[const.TAIL] % i,
                        self.ini_path(const.BLANK),
                    )
                    continue

                full_image_name = builder.full_image_name(element)

                if full_image_name not in self.images:
                    self.images.add(full_image_name)
                    res = builder.make(element)

                    res.save(self.asset_path_2x(full_image_name))
                    res.resize((res.width // 2, res.height // 2)).save(
                        self.asset_path(full_image_name)
                    )

                self.write_entry(
                    const.ELEMENT_MAP[element] % i,
                    self.ini_path(full_image_name),
                )

        self.write_line()
        self.write_line()


def build_skin(skin_name: str):
    return SkinBuilder(skin_name).build()
