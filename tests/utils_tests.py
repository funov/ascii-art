import unittest
from unittest.mock import patch, mock_open
from model.utils import write_ascii_art


class UtilsTests(unittest.TestCase):
    def setUp(self):
        self.expected_write_data_with_out_folder_win = ['###///###\n///###///']
        self.expected_folder_info_with_out_folder_win = [
            ('C:\\Users\\User\\folder\\image.txt', 'w')
        ]

        self.expected_write_data_with_out_folder_not_win = ['###///###\n///###///']
        self.expected_folder_info_with_out_folder_not_win = [
            ('C:/Users/User/folder/image.txt', 'w')
        ]

        self.expected_write_data_without_out_folder_win = ['###///###\n///###///']
        self.expected_folder_info_without_out_folder_win = [
            ('C:\\Users\\User\\image.txt', 'w')
        ]

        self.expected_write_data_without_out_folder_not_win = ['###///###\n///###///']
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

        self.assertEqual(self.expected_folder_info_with_out_folder_win, folder_info)
        self.assertEqual(self.expected_write_data_with_out_folder_win, write_data)

    def test_write_with_out_folder_not_win(self):
        m = mock_open()

        with patch('model.utils.open', m):
            write_ascii_art(
                '###///###\n///###///',
                'C:/Users/User/image.png',
                'C:/Users/User/folder'
            )

        folder_info, write_data = UtilsTests.get_info(m)

        self.assertEqual(self.expected_folder_info_with_out_folder_not_win, folder_info)
        self.assertEqual(self.expected_write_data_with_out_folder_not_win, write_data)

    def test_write_without_out_folder_win(self):
        m = mock_open()

        with patch('model.utils.open', m):
            write_ascii_art(
                '###///###\n///###///',
                'C:\\Users\\User\\image.png',
                None
            )

        folder_info, write_data = UtilsTests.get_info(m)

        self.assertEqual(self.expected_folder_info_without_out_folder_win, folder_info)
        self.assertEqual(self.expected_write_data_without_out_folder_win, write_data)

    def test_write_without_out_folder_not_win(self):
        m = mock_open()

        with patch('model.utils.open', m):
            write_ascii_art(
                '###///###\n///###///',
                'C:/Users/User/image.png',
                None
            )

        folder_info, write_data = UtilsTests.get_info(m)

        self.assertEqual(self.expected_folder_info_without_out_folder_not_win, folder_info)
        self.assertEqual(self.expected_write_data_without_out_folder_not_win, write_data)

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
