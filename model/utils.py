import os


def write_ascii_art(ascii_art, image_path, out_folder_path):
    if os.sep in image_path:
        image_name = image_path.split(os.sep)[-1]
    else:
        image_name = image_path.split('/')[-1]

    file_name = image_name[:image_name.rfind('.')] + '.txt'

    if out_folder_path is None:
        out_folder_path = image_path.replace(image_name, file_name)
    elif os.sep in out_folder_path:
        out_folder_path = os.path.join(out_folder_path, file_name)
    else:
        out_folder_path += '/' + file_name

    with open(out_folder_path, "w") as file:
        file.write(ascii_art)
