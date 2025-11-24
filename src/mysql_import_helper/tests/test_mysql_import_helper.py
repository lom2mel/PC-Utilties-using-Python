"""
Comprehensive unit tests for MySQL Import Helper.

Tests cover security validation, input validation, error handling,
and core functionality with proper mocking.
"""

import pytest
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from mysql_import_helper.mysql_import_helper import MySQLImportHelper


class TestMySQLImportHelper:
    """Test suite for MySQLImportHelper class."""

    def test_initialization_with_valid_parameters(self):
        """Test successful initialization with valid parameters."""
        helper = MySQLImportHelper(
            host="localhost",
            port=3306,
            user="root",
            password=None
        )
        assert helper.host == "localhost"
        assert helper.port == 3306
        assert helper.user == "root"
        assert helper.password is None
        assert helper.mysql_exe == "mysql.exe"

    def test_initialization_with_password(self):
        """Test initialization with password."""
        helper = MySQLImportHelper(
            host="localhost",
            port=3306,
            user="testuser",
            password="testpass"
        )
        assert helper.password == "testpass"

    def test_initialization_with_invalid_hostname(self):
        """Test initialization fails with invalid hostname."""
        with pytest.raises(ValueError, match="Invalid hostname"):
            MySQLImportHelper(host="invalid'host")

        with pytest.raises(ValueError, match="Invalid hostname"):
            MySQLImportHelper(host="")

    def test_initialization_with_invalid_port(self):
        """Test initialization fails with invalid port."""
        with pytest.raises(ValueError, match="Port must be between"):
            MySQLImportHelper(port=0)

        with pytest.raises(ValueError, match="Port must be between"):
            MySQLImportHelper(port=65536)

        with pytest.raises(ValueError, match="Port must be between"):
            MySQLImportHelper(port="invalid")

    def test_initialization_with_invalid_username(self):
        """Test initialization fails with invalid username."""
        with pytest.raises(ValueError, match="Invalid username"):
            MySQLImportHelper(user="")

        with pytest.raises(ValueError, match="Invalid username"):
            MySQLImportHelper(user="invalid@user")

    def test_is_valid_hostname(self):
        """Test hostname validation."""
        helper = MySQLImportHelper()

        # Valid hostnames
        assert helper._is_valid_hostname("localhost") is True
        assert helper._is_valid_hostname("example.com") is True
        assert helper._is_valid_hostname("192.168.1.1") is True
        assert helper._is_valid_hostname("my-server") is True

        # Invalid hostnames
        assert helper._is_valid_hostname("") is False
        assert helper._is_valid_hostname("a" * 254) is False  # Too long
        assert helper._is_valid_hostname("invalid'host") is False
        assert helper._is_valid_hostname("invalid;host") is False

    def test_validate_database_name(self):
        """Test database name validation."""
        helper = MySQLImportHelper()

        # Valid database names
        assert helper._validate_database_name("test_db") is True
        assert helper._validate_database_name("my-database") is True
        assert helper._validate_database_name("db123") is True
        assert helper._validate_database_name("a") is True

        # Invalid database names
        assert helper._validate_database_name("") is False
        assert helper._validate_database_name("a" * 65) is False  # Too long
        assert helper._validate_database_name("invalid;db") is False
        assert helper._validate_database_name("invalid db") is False
        assert helper._validate_database_name("invalid'db") is False

    @patch('subprocess.run')
    def test_run_mysql_command_success_without_password(self, mock_subprocess):
        """Test successful MySQL command execution without password."""
        mock_subprocess.return_value = Mock(returncode=0, stderr="")

        helper = MySQLImportHelper(password=None)
        result = helper.run_mysql_command("SHOW DATABASES;")

        assert result is True
        mock_subprocess.assert_called_once()
        args = mock_subprocess.call_args[0][0]  # Get the command args

        assert "--skip-password" in args
        assert "SHOW DATABASES;" in args

    @patch('subprocess.run')
    def test_run_mysql_command_success_with_password(self, mock_subprocess):
        """Test successful MySQL command execution with password."""
        mock_subprocess.return_value = Mock(returncode=0, stderr="")

        helper = MySQLImportHelper(password="testpass")
        result = helper.run_mysql_command("SHOW DATABASES;")

        assert result is True
        mock_subprocess.assert_called_once()

        # Check that password is passed via input, not command line
        assert mock_subprocess.call_args[1]['input'] == b"testpass"

    @patch('subprocess.run')
    def test_run_mysql_command_failure(self, mock_subprocess):
        """Test MySQL command execution failure."""
        mock_subprocess.return_value = Mock(returncode=1, stderr="Access denied")

        helper = MySQLImportHelper()
        result = helper.run_mysql_command("INVALID COMMAND")

        assert result is False

    @patch('subprocess.run')
    def test_run_mysql_command_file_not_found(self, mock_subprocess):
        """Test MySQL command when executable not found."""
        mock_subprocess.side_effect = FileNotFoundError()

        helper = MySQLImportHelper()
        result = helper.run_mysql_command("SHOW DATABASES;")

        assert result is False

    def test_run_mysql_command_invalid_database_name(self):
        """Test command execution with invalid database name."""
        helper = MySQLImportHelper()

        with pytest.raises(ValueError, match="Invalid database name"):
            helper.run_mysql_command("SHOW TABLES;", database="invalid'db")

    def test_run_mysql_command_invalid_command(self):
        """Test command execution with invalid command."""
        helper = MySQLImportHelper()

        with pytest.raises(ValueError, match="Invalid command"):
            helper.run_mysql_command("")

        with pytest.raises(ValueError, match="Invalid command"):
            helper.run_mysql_command("a" * 10001)  # Too long

    @patch.object(MySQLImportHelper, 'run_mysql_command')
    def test_create_database_success(self, mock_run_command):
        """Test successful database creation."""
        mock_run_command.return_value = True

        helper = MySQLImportHelper()
        result = helper.create_database("test_db")

        assert result is True
        mock_run_command.assert_called_once()

        # Check that the SQL command is properly formatted
        call_args = mock_run_command.call_args[0]
        assert "CREATE DATABASE IF NOT EXISTS `test_db`" in call_args[0]
        assert "utf8mb4" in call_args[0]

    def test_create_database_invalid_name(self):
        """Test database creation with invalid name."""
        helper = MySQLImportHelper()

        with pytest.raises(ValueError, match="Invalid database name"):
            helper.create_database("invalid'db")

    def test_extract_database_names_valid_directory(self):
        """Test extracting database names from valid directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test SQL files
            temp_path = Path(temp_dir)
            (temp_path / "test_db_table1.sql").touch()
            (temp_path / "test_db_table2.sql").touch()
            (temp_path / "other_db_data.sql").touch()
            (temp_path / "invalid'name.sql").touch()  # Should be skipped
            (temp_path / "readme.txt").touch()  # Non-SQL file

            helper = MySQLImportHelper()
            databases = helper.extract_database_names(temp_path)

            assert "test_db" in databases
            assert "other_db" in databases
            assert len(databases) == 2

    def test_extract_database_names_invalid_directory(self):
        """Test extracting database names from invalid directory."""
        helper = MySQLImportHelper()

        with pytest.raises(ValueError, match="Invalid dump directory"):
            helper.extract_database_names(Path("/nonexistent/directory"))

        with tempfile.NamedTemporaryFile() as temp_file:
            with pytest.raises(ValueError, match="Invalid dump directory"):
                helper.extract_database_names(Path(temp_file.name))

    def test_extract_database_names_empty_directory(self):
        """Test extracting database names from empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            helper = MySQLImportHelper()
            databases = helper.extract_database_names(Path(temp_dir))

            assert databases == set()

    @patch('builtins.open', new_callable=mock_open, read_data="CREATE TABLE test (id INT);")
    @patch('subprocess.run')
    def test_import_dump_file_success(self, mock_subprocess, mock_file):
        """Test successful dump file import."""
        mock_subprocess.return_value = Mock(returncode=0, stderr="")

        with tempfile.NamedTemporaryFile(suffix=".sql", delete=False) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            helper = MySQLImportHelper()
            result = helper.import_dump_file(temp_path, "test_db")

            assert result is True
            mock_file.assert_called_once()
            mock_subprocess.assert_called_once()
        finally:
            temp_path.unlink()

    def test_import_dump_file_invalid_file(self):
        """Test import with invalid file path."""
        helper = MySQLImportHelper()

        with pytest.raises(ValueError, match="Invalid dump file"):
            helper.import_dump_file(Path("/nonexistent/file.sql"), "test_db")

    def test_import_dump_file_invalid_database(self):
        """Test import with invalid database name."""
        with tempfile.NamedTemporaryFile(suffix=".sql") as temp_file:
            helper = MySQLImportHelper()

            with pytest.raises(ValueError, match="Invalid database name"):
                helper.import_dump_file(Path(temp_file.name), "invalid'db")

    def test_import_dump_file_too_large(self):
        """Test import with oversized file."""
        with tempfile.NamedTemporaryFile(suffix=".sql") as temp_file:
            # Mock file size to be larger than 100MB
            with patch('pathlib.Path.stat') as mock_stat:
                mock_stat.return_value.st_size = 150 * 1024 * 1024  # 150MB

                helper = MySQLImportHelper()

                with pytest.raises(ValueError, match="Dump file too large"):
                    helper.import_dump_file(Path(temp_file.name), "test_db")

    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_import_dump_file_empty_file(self, mock_file):
        """Test import with empty dump file."""
        with tempfile.NamedTemporaryFile(suffix=".sql", delete=False) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            helper = MySQLImportHelper()

            with pytest.raises(ValueError, match="Empty dump file"):
                helper.import_dump_file(temp_path, "test_db")
        finally:
            temp_path.unlink()

    @patch('builtins.open', new_callable=mock_open, read_data="a" * 60 * 1024 * 1024)  # 60MB content
    def test_import_dump_file_content_too_large(self, mock_file):
        """Test import with file content too large."""
        with tempfile.NamedTemporaryFile(suffix=".sql", delete=False) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            helper = MySQLImportHelper()

            with pytest.raises(ValueError, match="Dump file content too large"):
                helper.import_dump_file(temp_path, "test_db")
        finally:
            temp_path.unlink()

    @patch.object(MySQLImportHelper, 'extract_database_names')
    @patch.object(MySQLImportHelper, 'create_database')
    @patch.object(MySQLImportHelper, 'import_dump_file')
    def test_process_dump_directory_no_auto_import(self, mock_import, mock_create, mock_extract):
        """Test processing dump directory without auto-import."""
        mock_extract.return_value = {"test_db", "other_db"}
        mock_create.return_value = True

        with tempfile.TemporaryDirectory() as temp_dir:
            helper = MySQLImportHelper()
            helper.process_dump_directory(Path(temp_dir), auto_import=False)

            mock_extract.assert_called_once()
            # create_database should be called for each database
            assert mock_create.call_count == 2
            # import_dump_file should not be called
            mock_import.assert_not_called()

    @patch('pathlib.Path.glob')
    def test_process_dump_directory_nonexistent_directory(self, mock_glob):
        """Test processing nonexistent dump directory."""
        mock_glob.return_value = []

        helper = MySQLImportHelper()
        helper.process_dump_directory(Path("/nonexistent"), auto_import=False)

        # Should not raise exception, just print error message

    @patch.object(MySQLImportHelper, 'extract_database_names')
    def test_process_dump_directory_no_databases_found(self, mock_extract):
        """Test processing dump directory with no databases found."""
        mock_extract.return_value = set()

        with tempfile.TemporaryDirectory() as temp_dir:
            helper = MySQLImportHelper()
            helper.process_dump_directory(Path(temp_dir), auto_import=False)

            mock_extract.assert_called_once()


class TestMainFunction:
    """Test suite for main function."""

    @patch('sys.argv', ['mysql_import_helper.py', '/test/path'])
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_dir')
    @patch('getpass.getpass')
    @patch.object(MySQLImportHelper, 'process_dump_directory')
    def test_main_function_success(self, mock_process, mock_getpass, mock_is_dir, mock_exists):
        """Test successful main function execution."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        mock_getpass.return_value = "testpass"

        # Import and run main function
        from mysql_import_helper.mysql_import_helper import main

        # Should not raise exception
        main()

        mock_process.assert_called_once()

    @patch('sys.argv', ['mysql_import_helper.py', '/nonexistent/path'])
    @patch('pathlib.Path.exists')
    @patch('sys.exit')
    def test_main_function_nonexistent_directory(self, mock_exit, mock_exists):
        """Test main function with nonexistent directory."""
        mock_exists.return_value = False

        from mysql_import_helper.mysql_import_helper import main

        main()
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['mysql_import_helper.py', '/test/path'])
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_dir')
    @patch('getpass.getpass')
    def test_main_function_keyboard_interrupt(self, mock_getpass, mock_is_dir, mock_exists):
        """Test main function with keyboard interrupt."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        mock_getpass.side_effect = KeyboardInterrupt()

        from mysql_import_helper.mysql_import_helper import main

        with patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_once_with(0)

    @patch('sys.argv', ['mysql_import_helper.py', '/test/path'])
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_dir')
    @patch('getpass.getpass')
    @patch('sys.exit')
    def test_main_function_invalid_configuration(self, mock_exit, mock_getpass, mock_is_dir, mock_exists):
        """Test main function with invalid configuration."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        mock_getpass.return_value = "testpass"

        with patch('builtins.print'):  # Suppress print output
            from mysql_import_helper.mysql_import_helper import main
            from mysql_import_helper.mysql_import_helper import MySQLImportHelper

            # Mock MySQLImportHelper to raise ValueError
            with patch.object(MySQLImportHelper, '__init__', side_effect=ValueError("Invalid config")):
                main()
                mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    pytest.main([__file__])