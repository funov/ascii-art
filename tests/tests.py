import unittest
from unittest.mock import patch, mock_open
from PIL import Image
import numpy as np

from model.ascii_art_converter import ASCIIArtConverter
from model.utils import write_ascii_art


class UtilsTests(unittest.TestCase):
    def setUp(self):
        self.expected_write_data_with_out_folder_win = [
            '###///###\n///###///'
        ]
        self.expected_folder_info_with_out_folder_win = [
            ('C:\\Users\\User\\folder\\image.txt', 'w')
        ]

        self.expected_write_data_with_out_folder_not_win = [
            '###///###\n///###///'
        ]
        self.expected_folder_info_with_out_folder_not_win = [
            ('C:/Users/User/folder/image.txt', 'w')
        ]

        self.expected_write_data_without_out_folder_win = [
            '###///###\n///###///'
        ]
        self.expected_folder_info_without_out_folder_win = [
            ('C:\\Users\\User\\image.txt', 'w')
        ]

        self.expected_write_data_without_out_folder_not_win = [
            '###///###\n///###///'
        ]
        self.expected_folder_info_without_out_folder_not_win = [
            ('C:/Users/User/image.txt', 'w')
        ]

    def test_write_with_out_folder_win(self):
        m = mock_open()

        with patch('model.utils.open', m):
            write_ascii_art(
                '###///###\n///###///',
                'C:\\Users\\User\\image.png',
                'C:\\Users\\User\\folder'
            )

        folder_info, write_data = UtilsTests.get_info(m)

        self.assertEqual(
            self.expected_folder_info_with_out_folder_win,
            folder_info
        )
        self.assertEqual(
            self.expected_write_data_with_out_folder_win,
            write_data
        )

    def test_write_with_out_folder_not_win(self):
        m = mock_open()

        with patch('model.utils.open', m):
            write_ascii_art(
                '###///###\n///###///',
                'C:/Users/User/image.png',
                'C:/Users/User/folder'
            )

        folder_info, write_data = UtilsTests.get_info(m)

        self.assertEqual(
            self.expected_folder_info_with_out_folder_not_win,
            folder_info
        )
        self.assertEqual(
            self.expected_write_data_with_out_folder_not_win,
            write_data
        )

    def test_write_without_out_folder_win(self):
        m = mock_open()

        with patch('model.utils.open', m):
            write_ascii_art(
                '###///###\n///###///',
                'C:\\Users\\User\\image.png',
                None
            )

        folder_info, write_data = UtilsTests.get_info(m)

        self.assertEqual(
            self.expected_folder_info_without_out_folder_win,
            folder_info
        )
        self.assertEqual(
            self.expected_write_data_without_out_folder_win,
            write_data
        )

    def test_write_without_out_folder_not_win(self):
        m = mock_open()

        with patch('model.utils.open', m):
            write_ascii_art(
                '###///###\n///###///',
                'C:/Users/User/image.png',
                None
            )

        folder_info, write_data = UtilsTests.get_info(m)

        self.assertEqual(
            self.expected_folder_info_without_out_folder_not_win,
            folder_info
        )
        self.assertEqual(
            self.expected_write_data_without_out_folder_not_win,
            write_data
        )

    @staticmethod
    def get_info(m):
        calls = m.mock_calls

        folder_info = []
        write_data = []
        for call in calls:
            if call[0] == '().write':
                write_data.append(call[1][0])
            if call[0] == '':
                folder_info.append(call[1])

        return folder_info, write_data


class ASCIIArtConverterTests(unittest.TestCase):
    def setUp(self):
        image_array = np.array([
            [(155, 155, 155), (250, 250, 250), (155, 155, 155)],
            [(250, 250, 250), (155, 155, 155), (250, 250, 250)],
            [(155, 155, 155), (250, 250, 250), (155, 155, 155)]
        ]).astype('uint8')

        self.grayscale_image = Image.fromarray(image_array, mode='RGB')
        self.chars = '-/'
        self.not_different_chars = '----///'
        self.target = 10
        self.numbers = [2, 100, 500]

        self.expected_get_ascii_chars = [
            '/', '-', '/', '-', '/', '-', '/', '-', '/'
        ]
        self.expected_to_str_ascii_art = '/-/\n-/-\n/-/'
        self.expected_to_list_ascii_art = [
            ['/', '-', '/'],
            ['-', '/', '-'],
            ['/', '-', '/']
        ]
        self.expected_increase_contrast = [(250, 250, 250)] * 9
        self.expected_get_color_to_symbol_dict = {
            (250, 250, 250): '-',
            (155, 155, 155): '/'
        }
        self.expected_remove_similar_chars_list = [['/', '-'], ['-', '/']]
        self.expected_round_nearest_number = 2

    def test_get_ascii_chars(self):
        ascii_chars = ASCIIArtConverter.get_ascii_chars(
            self.grayscale_image,
            self.chars
        )

        self.assertEqual(self.expected_get_ascii_chars, ascii_chars)

    def test_to_str_ascii_art(self):
        str_ascii_art = ASCIIArtConverter.to_str_ascii_art(
            self.grayscale_image,
            self.chars
        )

        self.assertEqual(self.expected_to_str_ascii_art, str_ascii_art)

    def test_to_list_ascii_art(self):
        list_ascii_art = ASCIIArtConverter.to_list_ascii_art(
            self.grayscale_image,
            self.chars
        )

        self.assertEqual(self.expected_to_list_ascii_art, list_ascii_art)

    def test_increase_contrast(self):
        pixels = ASCIIArtConverter.increase_contrast(
            list(self.grayscale_image.getdata()),
            1,
            [(250, 250, 250), (155, 155, 155)]
        )

        self.assertEqual(self.expected_increase_contrast, pixels)

    def test_get_color_to_symbol_dict(self):
        color_to_symbol_dict = ASCIIArtConverter.get_color_to_symbol_dict(
            ['-', '/'],
            [(250, 250, 250), (155, 155, 155)]
        )

        self.assertEqual(
            self.expected_get_color_to_symbol_dict,
            color_to_symbol_dict
        )

    def test_remove_similar_chars(self):
        different_chars = ASCIIArtConverter.remove_similar_chars(
            self.not_different_chars
        )

        self.assertIn(
            different_chars,
            self.expected_remove_similar_chars_list
        )

    def test_round_nearest_number(self):
        rounded = ASCIIArtConverter.round_nearest_number(
            self.target,
            self.numbers
        )

        self.assertEqual(
            self.expected_round_nearest_number,
            rounded
        )
