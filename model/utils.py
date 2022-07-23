import os


def write_ascii_art(ascii_art, image_path, out_folder_path):
    image_name = image_path.split('/')[-1]
    file_name = image_name[:image_name.rfind('.')] + '.txt'

    if out_folder_path is None:
        out_folder_path = image_path.replace(image_name, file_name)
    else:
        out_folder_path += os.sep + file_name

    with open(out_folder_path, "w") as file:
        file.write(ascii_art)
