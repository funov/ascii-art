from model.image import MyImage
from model.ascii_art_converter import ASCIIArtConverter
from model.utils import write_ascii_art


class BaseController:
    @staticmethod
    def get_ascii_art(path, ascii_art_width, ascii_art_height, ascii_chars):
        image = MyImage(path)

        image.resize(ascii_art_width, ascii_art_height)
        image.to_gray_scale()

        ascii_art = ASCIIArtConverter.to_list_ascii_art(image.image, ascii_chars)

        return ascii_art

    @staticmethod
    def write_ascii_art(ascii_art, image_path, out_folder_path, is_console_output=False):
        if is_console_output:
            print(ascii_art)
        else:
            write_ascii_art(ascii_art, image_path, out_folder_path)
