from PIL import Image, ImageDraw, ImageOps

import osu_receptor.const as const
from osu_receptor.source import Source, Column
from osu_receptor.settings import Configuration


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
    def __init__(self, source: Source, column: Column, configuration: Configuration) -> None:
        self.skin = source
        self.token = column
        self.configuration = configuration

    def image_name_of(self, element: str):
        return self.token.elements[element]

    def image_of(self, element: str):
        return self.skin.images[self.image_name_of(element)]

    def full_image_name(self, element: str):
        return f"{self.image_name_of(element)}_{self.configuration.name}"

    def make(self, element: str):
        match element:
            case const.BODY if self.configuration.is_percy:
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
        partw = self.configuration.width * const.SCALE_FACTOR
        parth = partw * image.height / image.width
        partw, parth = int(partw), int(parth)
        partimg = image.resize((partw, parth))

        padx = int(xoff * self.configuration.spacing * const.SCALE_FACTOR)
        pady = int(yoff * self.configuration.hitpos * const.SCALE_FACTOR)

        return partimg.crop((-padx, -pady, partw + padx, parth + pady))

    def make_note(self, element: str):
        res = self.make_key(element, yoff=0)
        return res.crop((-1, 0, res.width - 1, res.height))

    def make_tail(self):
        res = self.make_note(const.TAIL)
        res = ImageOps.flip(res)

        if not self.notetail:
            res = res.crop((0, -res.height, res.width, res.height))

        return res

    def make_percy(self):
        body = self.make_note(const.BODY)
        tail = self.make_note(const.TAIL)
        start_height = tail.height // 2 if self.token.notetail else tail.height

        result = Image.new("RGBA", (body.width, const.PERCY_HEIGHT), "#0000")

        for y in range(start_height, const.PERCY_HEIGHT, body.height):
            result.paste(body, (0, y))

        result.paste(tail, (0, 0))

        return result
