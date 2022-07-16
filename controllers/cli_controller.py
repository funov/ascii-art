from ascii_art.image import MyImage
from ascii_art.ascii_art import ASCIIArt
from ascii_art.utils import write_ascii_art


def make_ascii_art(path, out_path, is_console_output, ascii_art_width, ascii_art_height, ascii_chars):
    image = MyImage(path)
    image.resize(ascii_art_width, ascii_art_height)
    image.to_gray_scale()

    ascii_art = ASCIIArt.to_ascii_art(image.image, ascii_chars)

    if is_console_output:
        print(ascii_art)
    else:
        write_ascii_art(ascii_art, path, out_path)
