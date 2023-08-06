from blacksheep import Request
from kikiutils.string import _RANDOM_LETTERS
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from random import choice, randint


file_path = Path(__file__).resolve()
font_path = str(file_path.parent / 'static' / 'arial.ttf')


# Vercode

class Vercode:
    bg_color = (0, 0, 0, 0)
    font_size = 32
    image_height = 50
    image_width = 150
    image_size = (image_width, image_height)
    vercode_length = 4

    font = ImageFont.truetype(font_path, size=font_size)
    font_base_x = (image_width - font_size * 4) / 2
    font_base_y = (image_height - font_size) / 2
    font_pos = []

    for i in range(vercode_length):
        font_pos.append((font_base_x + font_size * i, font_base_y))

    @classmethod
    def draw_line(cls, draw: ImageDraw.ImageDraw):
        for _ in range(6):
            pos = (
                randint(0, cls.image_width),
                randint(0, cls.image_width),
                randint(0, cls.image_height),
                randint(0, cls.image_height)
            )

            draw.line(pos, fill=cls.get_random_color())

    @classmethod
    def draw_point(cls, draw: ImageDraw.ImageDraw):
        for _ in range(20):
            pos = (randint(0, cls.image_width), randint(0, cls.image_height))
            draw.point(pos, fill=cls.get_random_color())

    @classmethod
    def get_random_color(cls):
        return (
            randint(0, 255),
            randint(0, 255),
            randint(0, 255),
            255
        )

    @classmethod
    def get_data(cls):
        image = Image.new('RGBA', color=cls.bg_color, size=cls.image_size)
        draw = ImageDraw.Draw(image)
        vercode = ''

        for i in range(cls.vercode_length):
            vercode += (random_char := choice(_RANDOM_LETTERS))
            char_color = cls.get_random_color()
            draw.text(
                cls.font_pos[i],
                text=random_char,
                fill=char_color,
                font=cls.font
            )

        cls.draw_line(draw)
        cls.draw_point(draw)
        return image, vercode

    @staticmethod
    def verify(rq: Request, vercode: str):
        session_vercode = rq.session.get('vercode', None)
        rq.session['vercode'] = None
        return vercode.lower() == session_vercode
