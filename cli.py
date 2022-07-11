import argparse
from image import make_ascii_art


def create_parser():
    description = "Из обычного изображения делает asсii-art"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        'path',
        help='Путь до изображения для asсii-art',
        type=str
    )
    parser.add_argument(
        '--out_path',
        '-op',
        help='Путь для вывода asсii-art в файл, если он не указан, '
             'то будет использован путь до исходного изображения',
        type=str,
        default=None
    )
    parser.add_argument(
        '--console',
        '-c',
        help='Отключить вывод в файл и вывести ascii-art на консоль',
        action='store_true')
    parser.add_argument(
        '--width',
        '-w',
        help='Ширина asсii-art изображения. Если указано, что-то одно '
             '(ширина или высота), то второе будет посчитано на основе '
             'пропорций исходного изображения. Если же не указано ничего, '
             'что за ширину и высоту будут взяты исходные размеры',
        type=int,
        default=None)
    parser.add_argument(
        '--height',
        '-he',
        help='Высота asсii-art изображения. Если указано, что-то одно '
             '(ширина или высота), то второе будет посчитано на основе '
             'пропорций исходного изображения. Если же не указано ничего, '
             'что за ширину и высоту будут взяты исходные размеры',
        type=int,
        default=None)
    parser.add_argument(
        '--chars',
        '-ch',
        help='Символы для asсii-art изображения',
        type=str,
        default='.,-=<>+?`*#')

    return parser


def main():
    parser = create_parser()
    cmd_commands = parser.parse_args()

    try:
        make_ascii_art(
            cmd_commands.path,
            cmd_commands.out_path,
            cmd_commands.console,
            cmd_commands.width,
            cmd_commands.height,
            cmd_commands.chars
        )
    except RuntimeError:
        print('Что-то пошло не так, напишите разработчикам')


if __name__ == '__main__':
    main()
