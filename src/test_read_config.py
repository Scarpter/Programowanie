import unittest
from unittest.mock import patch, mock_open

from src.unittest.read_config import read_config
config_data=    """key1=value1
    key2=value2
    key3=value3
    key4=value4
    """
class TestReadConfig(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='my_result')
    def test_read_config_uses_open(self, mock_file):

        expected_result={
    'key1':'value1',
    'key2':'value2',
    'key3':'value3',
    'key4':'value4'
    }
        result=read_config('config.ini')
        self.assertEqual(read_config('config.ini'), 'my_result')
        mock_file.assert_called_once_with('config.ini')


