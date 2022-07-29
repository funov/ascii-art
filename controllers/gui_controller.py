from controllers.base_controller import BaseController


def make_ascii_art(path, ascii_art_width, ascii_art_height, ascii_chars):
    return BaseController.get_ascii_art(path, ascii_art_width, ascii_art_height, ascii_chars)


def write(ascii_art, image_path, out_folder_path):
    BaseController.write_ascii_art(ascii_art, image_path, out_folder_path)
