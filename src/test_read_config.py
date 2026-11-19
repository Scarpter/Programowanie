import unittest
from unittest.mock import patch

from src.unittest.read_config import read_config

class TestReadConfig(unittest.TestCase):

    @patch("builtins.open")
    def test_read_config_uses_open(self, mock_open):
         # Mocking file opening so that read returns 'my_result'
         mock_open.return_value.__enter__.return_value.read.return_value = 'my_result'

         self.assertEqual(read_config('config.ini'), 'my_result')
         mock_open.assert_called_once_with('config.ini')


