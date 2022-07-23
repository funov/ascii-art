class ASCIIArtConverter:
    @staticmethod
    def get_ascii_chars(grayscale_image, chars):
        chars = ASCIIArtConverter.remove_similar_chars(chars)
        pixels = list(grayscale_image.getdata())

        different_pixels = list(set(pixels))
        different_pixels.sort(key=lambda p: pixels.count(p[0]), reverse=True)

        pixels = ASCIIArtConverter.increase_contrast(
            pixels,
            len(chars),
            different_pixels
        )
        color_to_symbol_dict = ASCIIArtConverter.get_color_to_symbol_dict(
            chars,
            different_pixels
        )

        new_pixels = [color_to_symbol_dict[pixel] for pixel in pixels]

        return new_pixels

    @staticmethod
    def to_str_ascii_art(grayscale_image, chars):
        width, height = grayscale_image.size
        ascii_chars = ASCIIArtConverter.get_ascii_chars(grayscale_image, chars)

        ascii_chars_str = ''.join(ascii_chars)

        chars_len = len(ascii_chars_str)
        ascii_image = [ascii_chars_str[i:i + width] for i in range(0, chars_len, width)]
        ascii_image = "\n".join(ascii_image)

        return ascii_image

    @staticmethod
    def to_list_ascii_art(grayscale_image, chars):
        width, height = grayscale_image.size
        ascii_chars = ASCIIArtConverter.get_ascii_chars(grayscale_image, chars)

        ascii_art_list = [ascii_chars[i:i + width] for i in range(0, len(ascii_chars), width)]

        return ascii_art_list

    @staticmethod
    def increase_contrast(pixels, color_count, different_pixels):
        pixels = pixels.copy()

        first = [different_pixels[j][0] for j in range(min(color_count, len(different_pixels)))]

        for i in range(len(pixels)):
            pixel = pixels[i][0]
            if pixel not in first:
                nearest_pixel = ASCIIArtConverter.round_nearest_number(
                    pixel,
                    first
                )
                pixels[i] = (nearest_pixel, nearest_pixel, nearest_pixel)

        return pixels

    @staticmethod
    def get_color_to_symbol_dict(chars, different_pixels):
        color_to_symbol = dict.fromkeys(
            [different_pixels[j] for j in range(min(len(chars), len(different_pixels)))]
        )

        k = 0
        for key in color_to_symbol.keys():
            color_to_symbol[key] = chars[k]
            k += 1

        return color_to_symbol

    @staticmethod
    def remove_similar_chars(c):
        return list(set(c)) if len(set(c)) != len(c) else list(c)

    @staticmethod
    def round_nearest_number(target, numbers):
        differences = [abs(target - number) for number in numbers]
        index_min_difference = differences.index(min(differences))
        return numbers[index_min_difference]
