import unittest
from unittest.mock import patch

from db.DB import DB
from db.db_config import DB_CONFIG, DB_NAME


class TestDB(unittest.TestCase):

    @patch("db.DB.mysql.connector.connect")
    def test_connect_with_database(self, mock_connect):
        DB.connect()

        expected = DB_CONFIG.copy()
        expected["database"] = DB_NAME

        mock_connect.assert_called_once_with(**expected)

    @patch("db.DB.mysql.connector.connect")
    def test_connect_without_database(self, mock_connect):
        DB.connect(use_db=False)

        mock_connect.assert_called_once_with(**DB_CONFIG)
