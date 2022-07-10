from PIL import Image


def prepare_image_for_ascii_art(image_path, new_width, new_height):
    img = Image.open(image_path).convert('RGB')

    width, height = img.size

    new_width, new_height = get_new_size(width, height, new_width, new_height)

    img = img.resize((new_width, new_height))

    gray_img = to_gray_scale(img)

    return gray_img


def get_new_size(width, height, new_width, new_height):
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
