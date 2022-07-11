from PIL import Image


def make_ascii_art(path, out_path, is_console_output, ascii_art_width, ascii_art_height, ascii_chars):
    image = prepare_image_for_ascii_art(path, ascii_art_width, ascii_art_height)
    ascii_art = to_ascii_art(image, ascii_chars)

    if is_console_output:
        print(ascii_art)
    else:
        write_ascii_art(ascii_art, path, out_path)


def to_ascii_art(image, chars):
    if len(set(chars)) != len(chars):
        chars = list(set(chars))
    pixels = image.getdata()

    width, height = image.size

    groups_count = int(255 / (len(chars) - 1))

    new_pixels = [chars[pixel[0] // groups_count] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + width] for index in range(0, new_pixels_count, width)]
    ascii_image = "\n".join(ascii_image)

    return ascii_image


def write_ascii_art(ascii_art, path, out_path):
    if out_path is None:
        out_path = path.split('.')[0]

    with open(out_path + '.txt', "w") as file:
        file.write(ascii_art)


def prepare_image_for_ascii_art(image_path, new_width, new_height):
    img = Image.open(image_path).convert('RGB')

    width, height = img.size

    new_width, new_height = get_new_image_size(width, height, new_width, new_height)

    img = img.resize((new_width, new_height))

    new_img = to_gray_scale(img)

    return new_img


def get_new_image_size(width, height, new_width, new_height):
    if new_width is None and new_height is None:
        new_width = width
        new_height = height
    elif new_height is None:
        aspect_ratio = height / width
        new_height = int(aspect_ratio * new_width * 0.55)
    elif new_width is None:
        aspect_ratio = width / height
        new_width = int(aspect_ratio * new_height * 1.45)

    return new_width, new_height


def to_gray_scale(image):
    image = image.copy()
    w, h = image.size

    for x in range(w):
        for y in range(h):
            data = image.getpixel((x, y))
            gray = to_gray(data[0], data[1], data[2])
            image.putpixel((x, y), (gray, gray, gray))

    return image


def to_gray(r, g, b):
    return int(0.2126 * r + 0.7152 * g + 0.0722 * b)
