from ascii_art.image import MyImage
from ascii_art.ascii_art import ASCIIArt
from ascii_art.utils import write_ascii_art


def make_ascii_art(path, ascii_art_width, ascii_art_height, ascii_chars):
    image = MyImage(path)
    image.resize(ascii_art_width, ascii_art_height)
    image.to_gray_scale()

    ascii_art = ASCIIArt.to_ascii_art(image.image, ascii_chars)

    return ascii_art


def write(ascii_art, out_path):
    write_ascii_art(ascii_art, None, out_path)
