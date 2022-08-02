from controllers.base_controller import BaseController


def make_ascii_art(
        path,
        out_path,
        is_console_output,
        ascii_art_width,
        ascii_art_height,
        ascii_chars):
    try:
        ascii_art = BaseController.get_ascii_art(
            path,
            ascii_art_width,
            ascii_art_height,
            ascii_chars
        )
        BaseController.write_ascii_art(
            ascii_art,
            path,
            out_path,
            is_console_output
        )
    except OSError:
        print('Некорректный файловый путь')
