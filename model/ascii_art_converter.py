class ASCIIArtConverter:
    @staticmethod
    def to_ascii_art(grayscale_image, chars):
        chars = ASCIIArtConverter.remove_similar_chars(chars)
        pixels = list(grayscale_image.getdata())

        width, height = grayscale_image.size

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
        new_pixels = ''.join(new_pixels)

        c = len(new_pixels)
        ascii_image = [new_pixels[i:i + width] for i in range(0, c, width)]
        ascii_image = "\n".join(ascii_image)

        return ascii_image

    @staticmethod
    def increase_contrast(pixels, color_count, different_pixels):
        pixels = pixels.copy()

        first = [different_pixels[j][0] for j in range(color_count)]

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
            [different_pixels[j] for j in range(len(chars))]
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
