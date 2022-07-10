import argparse
from ascii_art.converter import make_ascii_art


def create_parser():
    description = "Из обычной картинки делает картинку из символов, т.е. askii-art"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('path', help='Путь к картинке для askii-art', type=str)
    parser.add_argument('--out_path',
                        '-o',
                        help='Путь для вывода askii-art результата в файл',
                        type=str,
                        default=None)
    parser.add_argument('--result',
                        '-r',
                        help='Вывод askii-art результата',
                        type=str,
                        choices=['file', 'console'],
                        default='file')
    parser.add_argument('--width',
                        '-w',
                        help='Ширина askii-art изображения',
                        type=int,
                        default=None)
    parser.add_argument('--height',
                        '-h',
                        help='Высота askii-art изображения',
                        type=int,
                        default=None)
    parser.add_argument('--chars',
                        '-c',
                        help='Символы для askii-art изображения',
                        type=str,
                        default='#&@$%')

    return parser


def main():
    parser = create_parser()
    cmd_commands = parser.parse_args()

    try:
        make_ascii_art(
            cmd_commands.path,
            cmd_commands.out_path,
            cmd_commands.result,
            cmd_commands.width,
            cmd_commands.height,
            cmd_commands.chars
        )
    except RuntimeError:
        print('Что-то пошло не так, напишите разработчикам')


if __name__ == '__main__':
    main()
