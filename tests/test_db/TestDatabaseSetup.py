import unittest
from unittest.mock import MagicMock, patch

from db.db_config import DB_NAME
from db.setup_db import (
    create_database,
    create_address_table,
    create_person_table
)


class TestDatabaseSetup(unittest.TestCase):

    @patch("db.setup_db.DB.connect")
    def test_create_database(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        create_database()

        mock_cursor.execute.assert_called_once_with(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
        )

    @patch("db.setup_db.DB.connect")
    def test_create_address_table(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        create_address_table()

        mock_cursor.execute.assert_any_call(f"USE {DB_NAME}")

        self.assertTrue(
            any("CREATE TABLE IF NOT EXISTS address" in call.args[0]
                for call in mock_cursor.execute.call_args_list)
        )

        mock_conn.commit.assert_called_once()

    @patch("db.setup_db.DB.connect")
    def test_create_person_table(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        create_person_table()

        mock_cursor.execute.assert_any_call(f"USE {DB_NAME}")

        self.assertTrue(
            any("CREATE TABLE IF NOT EXISTS person" in call.args[0]
                for call in mock_cursor.execute.call_args_list)
        )

        mock_conn.commit.assert_called_once()
