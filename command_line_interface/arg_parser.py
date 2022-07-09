import argparse


def create_parser():
    description = "Из обычной картинки делает картинку из символов"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('path', help='Путь к картинке', type=str)
    parser.add_argument('--result',
                        '-r',
                        help='Вывод результата',
                        type=str,
                        choices=['file', 'console'],
                        default='file')
    parser.add_argument('--width',
                        '-w',
                        help='Ширина askii-art изображения',
                        type=int,
                        default=None)

    return parser


def main():
    parser = create_parser()
    cmd_commands = parser.parse_args()

    try:
        pass
    except RuntimeError:
        print('Что-то пошло не так, напишите разработчикам')


if __name__ == '__main__':
    main()
