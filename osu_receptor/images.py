from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

import osu_receptor.const as const
from osu_receptor.settings import Layout
from osu_receptor.skin import Skin, Column


def make_blank():
    return Image.new("RGBA", (1, 1), "#0000")


def make_cover(width: int, height: int, pattern: list[Column]):
    cover = Image.new("RGBA", (width * len(pattern), const.HEIGHT))
    draw = ImageDraw.Draw(cover)

    for i, token in enumerate(pattern):
        xm = i * width
        xM = (i + 1) * width - 1
        *rgb, _ = token.color
        draw.rectangle((xm, 0, xM, height), tuple(rgb))

    return cover


class ImageBuilder:
    def __init__(self, skin: Skin, column: Column, layout: Layout) -> None:
        self.skin = skin
        self.column = column
        self.layout = layout

    def image_name_of(self, element: str) -> Path:
        return self.column.elements[element]

    def image_of(self, element: str) -> Image.Image | None:
        return self.skin.images[self.image_name_of(element)]

    def full_image_name(self, element: str):
        return f"{self.image_name_of(element).stem}_{self.layout.id}"

    def make(self, element: str):
        match element:
            case const.BODY if self.layout.is_percy:
                return self.make_percy()

            case const.TAIL:
                return self.make_tail()

            case const.KEYUP | const.KEYDOWN:
                return self.make_key(element)

            case const.NOTE | const.HEAD | const.BODY:
                return self.make_note(element)

        raise ValueError(f"unexpected element for configuration: {element}")

    def make_key(self, element: str, xoff=1, yoff=1):
        image = self.image_of(element)
        assert image is not None, f"image for {element} does not exist"

        partw = self.layout.width * const.SCALE_FACTOR
        parth = partw * image.height / image.width
        partw, parth = int(partw), int(parth)
        partimg = image.resize((partw, parth))

        padx = int(xoff * self.layout.spacing * const.SCALE_FACTOR)
        pady = int(yoff * self.layout.hitpos * const.SCALE_FACTOR)

        return partimg.crop((-padx, -pady, partw + padx, parth + pady))

    def make_note(self, element: str):
        res = self.make_key(element, yoff=0)
        return res.crop((-1, 0, res.width - 1, res.height))

    def make_tail(self):
        res = self.make_note(const.TAIL)
        res = ImageOps.flip(res)

        if not self.column.notetail:
            res = res.crop((0, -res.height, res.width, res.height))

        return res

    def make_percy(self):
        body = self.make_note(const.BODY)
        tail = self.make_note(const.TAIL)
        start_height = tail.height // 2 if self.column.notetail else tail.height

        result = Image.new("RGBA", (body.width, const.PERCY_HEIGHT), "#0000")

        for y in range(start_height, const.PERCY_HEIGHT, body.height):
            result.paste(body, (0, y))

        result.paste(tail, (0, 0))

        return result
