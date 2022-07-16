class ASCIIArt:
    @staticmethod
    def to_ascii_art(grayscale_image, chars):
        chars = ASCIIArt.remove_similar_chars(chars)
        pixels = list(grayscale_image.getdata())

        width, height = grayscale_image.size

        different_pixels = list(set(pixels))
        different_pixels.sort(key=lambda p: pixels.count(p[0]), reverse=True)

        pixels = ASCIIArt.increase_contrast(pixels, len(chars), different_pixels)
        color_to_symbol_dict = ASCIIArt.get_color_to_symbol_dict(chars, different_pixels)

        new_pixels = [color_to_symbol_dict[pixel] for pixel in pixels]
        new_pixels = ''.join(new_pixels)

        new_pixels_count = len(new_pixels)
        ascii_image = [new_pixels[index:index + width] for index in range(0, new_pixels_count, width)]
        ascii_image = "\n".join(ascii_image)

        return ascii_image

    @staticmethod
    def increase_contrast(pixels, color_count, different_pixels):
        pixels = pixels.copy()

        first = [different_pixels[j][0] for j in range(color_count)]

        for i in range(len(pixels)):
            pixel = pixels[i][0]
            if pixel not in first:
                nearest_pixel = ASCIIArt.round_nearest_number(pixel, first)
                pixels[i] = (nearest_pixel, nearest_pixel, nearest_pixel)

        return pixels

    @staticmethod
    def get_color_to_symbol_dict(chars, different_pixels):
        color_to_symbol_dict = dict.fromkeys([different_pixels[j] for j in range(len(chars))])

        k = 0
        for key in color_to_symbol_dict.keys():
            color_to_symbol_dict[key] = chars[k]
            k += 1

        return color_to_symbol_dict

    @staticmethod
    def remove_similar_chars(chars):
        return list(set(chars)) if len(set(chars)) != len(chars) else list(chars)

    @staticmethod
    def round_nearest_number(target, numbers):
        differences = [abs(target - number) for number in numbers]
        index_min_difference = differences.index(min(differences))
        return numbers[index_min_difference]
