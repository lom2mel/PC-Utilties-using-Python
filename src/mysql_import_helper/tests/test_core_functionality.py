"""
Core functionality tests for MySQL Import Helper.

Focuses on testing the validation and security improvements.
"""

import pytest
from pathlib import Path
import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from mysql_import_helper.mysql_import_helper import MySQLImportHelper


class TestValidation:
    """Test validation and security functionality."""

    def test_valid_hostnames(self):
        """Test that valid hostnames are accepted."""
        helper = MySQLImportHelper()
        valid_hostnames = [
            "localhost",
            "example.com",
            "192.168.1.1",
            "my-server",
            "db.company.org",
            "test-db-1"
        ]

        for hostname in valid_hostnames:
            assert helper._is_valid_hostname(hostname), f"Should accept: {hostname}"

    def test_invalid_hostnames(self):
        """Test that invalid hostnames are rejected."""
        helper = MySQLImportHelper()
        invalid_hostnames = [
            "",
            "a" * 254,  # Too long
            "invalid'host",
            "invalid;host",
            "invalid`host",
            "invalid$host",
            "invalid host",  # Contains space
            "host\nname",  # Contains newline
        ]

        for hostname in invalid_hostnames:
            assert not helper._is_valid_hostname(hostname), f"Should reject: {hostname}"

    def test_valid_database_names(self):
        """Test that valid database names are accepted."""
        helper = MySQLImportHelper()
        valid_names = [
            "test",
            "test_db",
            "my-database",
            "db123",
            "a",
            "test_database_1",
            "DB_NAME",
            "test-db-123",
        ]

        for name in valid_names:
            assert helper._validate_database_name(name), f"Should accept: {name}"

    def test_invalid_database_names(self):
        """Test that invalid database names are rejected."""
        helper = MySQLImportHelper()
        invalid_names = [
            "",
            "a" * 65,  # Too long
            "invalid'db",
            "invalid;db",
            "invalid`db",
            "invalid$db",
            "invalid db",  # Contains space
            "db\nname",  # Contains newline
            "db,name",  # Contains comma
        ]

        for name in invalid_names:
            assert not helper._validate_database_name(name), f"Should reject: {name}"

    def test_initialization_validation(self):
        """Test that initialization properly validates inputs."""
        # Valid initialization
        helper = MySQLImportHelper(
            host="localhost",
            port=3306,
            user="root",
            password=None
        )
        assert helper.host == "localhost"
        assert helper.port == 3306
        assert helper.user == "root"

        # Invalid hostname
        with pytest.raises(ValueError, match="Invalid hostname"):
            MySQLImportHelper(host="invalid'host")

        # Invalid port
        with pytest.raises(ValueError, match="Port must be between"):
            MySQLImportHelper(port=0)

        with pytest.raises(ValueError, match="Port must be between"):
            MySQLImportHelper(port=65536)

        # Invalid username
        with pytest.raises(ValueError, match="Invalid username"):
            MySQLImportHelper(user="")

        with pytest.raises(ValueError, match="Invalid username"):
            MySQLImportHelper(user="invalid@user")


class TestSecurity:
    """Test security-related functionality."""

    def test_password_not_exposed_in_command_line(self):
        """Test that passwords are not exposed in command line arguments."""
        helper = MySQLImportHelper(password="secret123")

        # Mock subprocess to capture command arguments
        import subprocess
        from unittest.mock import Mock

        # Create a mock that will capture the call arguments
        original_run = subprocess.run
        captured_args = []

        def mock_run(*args, **kwargs):
            captured_args.extend(args)
            # Return a successful result
            result = Mock()
            result.returncode = 0
            result.stderr = ""
            return result

        subprocess.run = mock_run

        try:
            helper.run_mysql_command("SHOW DATABASES;")

            # Check that the command was called
            assert len(captured_args) > 0

            # Get the command arguments (first element of first call)
            cmd = captured_args[0]

            # Password should not be in the command line
            assert "--password" in cmd
            password_index = cmd.index("--password")

            # Password should be passed via stdin, not command line
            # So the next item should NOT be the password
            if password_index + 1 < len(cmd):
                assert cmd[password_index + 1] != "secret123"

        finally:
            # Restore original function
            subprocess.run = original_run

    def test_command_argument_escaping(self):
        """Test that command arguments are properly escaped."""
        helper = MySQLImportHelper()

        # Test with database name that could be used for injection
        with pytest.raises(ValueError, match="Invalid database name"):
            helper.run_mysql_command("SHOW TABLES;", database="test'; DROP TABLE users; --")

        # Test with empty command
        with pytest.raises(ValueError, match="Invalid command"):
            helper.run_mysql_command("")

    def test_sql_injection_prevention(self):
        """Test that SQL injection attempts are prevented."""
        helper = MySQLImportHelper()

        # Test database creation with injection attempts
        injection_attempts = [
            "test'; DROP TABLE users; --",
            "test`--",
            "test; DELETE FROM users; --",
            "test' OR '1'='1",
        ]

        for injection in injection_attempts:
            with pytest.raises(ValueError, match="Invalid database name"):
                helper.create_database(injection)


class TestErrorHandling:
    """Test error handling."""

    def test_validation_error_messages(self):
        """Test that validation errors have clear messages."""
        # Hostname validation
        with pytest.raises(ValueError, match="Invalid hostname: test'host"):
            MySQLImportHelper(host="test'host")

        # Port validation
        with pytest.raises(ValueError, match="Port must be between 1 and 65535, got: 0"):
            MySQLImportHelper(port=0)

        # Username validation
        with pytest.raises(ValueError, match="Invalid username: test@user"):
            MySQLImportHelper(user="test@user")

    def test_database_name_validation_error_messages(self):
        """Test database name validation error messages."""
        helper = MySQLImportHelper()

        # The validation returns False, doesn't raise an exception
        assert not helper._validate_database_name("test'db")


class TestFileOperations:
    """Test file operations with security checks."""

    def test_extract_database_names_ignores_invalid_names(self):
        """Test that invalid database names are ignored during extraction."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test files with various names
            (temp_path / "valid_db.sql").touch()
            (temp_path / "invalid'db.sql").touch()
            (temp_path / "another_valid.sql").touch()
            (temp_path / "test;db.sql").touch()  # Invalid - contains semicolon

            helper = MySQLImportHelper()
            databases = helper.extract_database_names(temp_path)

            # Should only contain valid database names
            assert "valid" in databases  # Extracted from "valid_db"
            assert "another" in databases  # Extracted from "another_valid"
            assert "invalid" not in databases  # Should not include part of invalid name
            assert "test" not in databases  # Should not include part of invalid name
            assert len(databases) == 2


# Import tempfile for test
import tempfile


if __name__ == '__main__':
    pytest.main([__file__, '-v'])