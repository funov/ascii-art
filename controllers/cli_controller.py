from model.image import MyImage
from model.ascii_art_converter import ASCIIArtConverter
from model.utils import write_ascii_art


def make_ascii_art(
        path,
        out_path,
        is_console_output,
        ascii_art_width,
        ascii_art_height,
        ascii_chars):
    image = MyImage(path)
    image.resize(ascii_art_width, ascii_art_height)
    image.to_gray_scale()

    ascii_art = ASCIIArtConverter.to_ascii_art(image.image, ascii_chars)

    if is_console_output:
        print(ascii_art)
    else:
        try:
            write_ascii_art(ascii_art, path, out_path)
        except OSError:
            print('Некорректный файловый путь')
