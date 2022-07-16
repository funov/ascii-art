def write_ascii_art(ascii_art, path, out_path):
    # МЕСТО ДЛЯ ОШИБКИ

    if out_path is None:
        out_path = path.split('.')[0]

    with open(out_path + '.txt', "w") as file:
        file.write(ascii_art)
