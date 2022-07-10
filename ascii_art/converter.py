from ascii_art.image import prepare_image_for_ascii_art


def make_ascii_art(path, out_path, result, new_width, new_height, chars):
    gray_img = prepare_image_for_ascii_art(path, new_width, new_height)
    ascii_art = to_ascii_art(gray_img, chars, new_width)
    show_result(ascii_art, result, path, out_path)


def to_ascii_art(gray_image, chars, new_width):
    chars = list(set(chars))
    pixels = gray_image.getdata()

    groups_count = int(255 / (len(chars) - 1))

    new_pixels = [chars[pixel[0] // groups_count] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)

    return ascii_image


def show_result(ascii_art, result, path, out_path):
    if result == 'file':
        if out_path is not None:
            a = out_path
        else:
            a = path

        with open(a + 'ascii_art.txt', "w") as f:
            f.write(ascii_art)
    elif result == 'console':
        print(ascii_art)
