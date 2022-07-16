from PIL import Image


class MyImage:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path).convert('RGB')

    def resize(self, new_width, new_height):
        new_width, new_height = self.calculate_image_size(new_width, new_height)
        self.image = self.image.resize((new_width, new_height))

    def calculate_image_size(self, new_width, new_height):
        width, height = self.image.size

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

    def to_gray_scale(self):
        width, height = self.image.size

        for x in range(width):
            for y in range(height):
                data = self.image.getpixel((x, y))
                gray = self.to_gray(data[0], data[1], data[2])
                self.image.putpixel((x, y), (gray, gray, gray))

    @staticmethod
    def to_gray(r, g, b):
        return int(0.2126 * r + 0.7152 * g + 0.0722 * b)
