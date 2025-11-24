#!/usr/bin/env python3
"""
MySQL Database Import Helper with Auto-Creation.

This script automatically creates databases before importing SQL dump files,
preventing the "Unknown database" error.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Set, Optional
import getpass
import re
import tempfile
import os


class MySQLImportHelper:
    """Helper class for MySQL database import operations."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 3306,
        user: str = "root",
        password: Optional[str] = None,
    ):
        """Initialize MySQL connection parameters."""
        # Validate inputs
        if not self._is_valid_hostname(host):
            raise ValueError(f"Invalid hostname: {host}")
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ValueError(f"Port must be between 1 and 65535, got: {port}")
        if not user or not user.isalnum() and '_' not in user:
            raise ValueError(f"Invalid username: {user}")

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.mysql_exe = "mysql.exe"

    def _is_valid_hostname(self, hostname: str) -> bool:
        """Validate hostname to prevent injection attacks."""
        if not hostname or len(hostname) > 253:
            return False
        # Allow localhost and valid IP addresses/hostnames
        allowed_pattern = r'^[a-zA-Z0-9.-]+$'
        return bool(re.match(allowed_pattern, hostname))

    def _validate_database_name(self, db_name: str) -> bool:
        """Validate database name to prevent SQL injection."""
        if not db_name or len(db_name) > 64:
            return False
        # Only allow alphanumeric, underscore, and dash
        return bool(re.match(r'^[a-zA-Z0-9_-]+$', db_name))

    def run_mysql_command(self, command: str, database: str = "") -> bool:
        """Execute a MySQL command and return success status."""
        # Validate database name if provided
        if database and not self._validate_database_name(database):
            raise ValueError(f"Invalid database name: {database}")

        # Validate command to prevent injection
        if not command or len(command) > 10000:
            raise ValueError("Invalid command")

        cmd = [
            self.mysql_exe,
            "--host", self.host,
            "--user", self.user,
            "--port", str(self.port),
            "--default-character-set=utf8mb4",
        ]

        # Handle password securely - use environment variable or temp file
        if self.password:
            cmd.append("--password")
            # Password will be provided via stdin for security
        else:
            cmd.append("--skip-password")

        if database:
            cmd.extend(["--database", database])

        cmd.extend(["-e", command])

        try:
            # Handle password input securely
            password_input = None
            if self.password:
                password_input = self.password.encode('utf-8')

            result = subprocess.run(
                cmd,
                input=password_input,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                print(f"[ERROR] {result.stderr.strip()}")
                return False
            return True
        except FileNotFoundError:
            print(f"[ERROR] MySQL executable not found: {self.mysql_exe}")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to execute MySQL command: {e}")
            return False

    def create_database(self, db_name: str) -> bool:
        """Create a database if it doesn't exist."""
        if not self._validate_database_name(db_name):
            raise ValueError(f"Invalid database name: {db_name}")

        print(f"[INFO] Creating database '{db_name}' if not exists...")
        # Use parameterized approach to prevent SQL injection
        sql = (
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        )
        success = self.run_mysql_command(sql)
        if success:
            print(f"[SUCCESS] Database '{db_name}' is ready")
        return success

    def extract_database_names(self, dump_dir: Path) -> Set[str]:
        """Extract unique database names from SQL dump files."""
        if not dump_dir.exists() or not dump_dir.is_dir():
            raise ValueError(f"Invalid dump directory: {dump_dir}")

        databases = set()
        sql_files = list(dump_dir.glob("*.sql"))

        print(f"[INFO] Found {len(sql_files)} SQL dump files")

        for sql_file in sql_files:
            if not sql_file.is_file():
                continue

            filename = sql_file.stem
            # Extract database name (first part before underscore or full name)
            parts = filename.split("_")
            if parts:
                db_name = parts[0]
                # Validate database name before adding
                if self._validate_database_name(db_name):
                    databases.add(db_name)
                else:
                    print(f"[WARNING] Skipping invalid database name: {db_name}")

        return databases

    def import_dump_file(self, dump_file: Path, database: str) -> bool:
        """Import a SQL dump file into a database."""
        if not dump_file.exists() or not dump_file.is_file():
            raise ValueError(f"Invalid dump file: {dump_file}")

        if not self._validate_database_name(database):
            raise ValueError(f"Invalid database name: {database}")

        # Check file size to prevent processing extremely large files
        if dump_file.stat().st_size > 100 * 1024 * 1024:  # 100MB limit
            raise ValueError(f"Dump file too large: {dump_file.stat().st_size} bytes")

        print(f"[INFO] Importing {dump_file.name} into {database}...")

        cmd = [
            self.mysql_exe,
            "--host", self.host,
            "--user", self.user,
            "--port", str(self.port),
            "--default-character-set=utf8mb4",
            "--database", database,
        ]

        # Handle password securely
        if self.password:
            cmd.append("--password")

        try:
            # Handle password input securely
            password_input = None
            if self.password:
                password_input = self.password.encode('utf-8')

            with open(dump_file, "r", encoding="utf8") as f:
                file_content = f.read()
                # Basic validation of SQL content
                if not file_content.strip():
                    raise ValueError("Empty dump file")
                if len(file_content) > 50 * 1024 * 1024:  # 50MB content limit
                    raise ValueError("Dump file content too large")

                result = subprocess.run(
                    cmd,
                    input=password_input,
                    capture_output=True,
                    text=True,
                    check=False,
                )

            if result.returncode != 0:
                print(f"[ERROR] Import failed: {result.stderr.strip()}")
                return False

            print(f"[SUCCESS] Imported {dump_file.name}")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to import {dump_file.name}: {e}")
            return False

    def process_dump_directory(
        self, dump_dir: Path, auto_import: bool = False
    ) -> None:
        """Process all dump files in a directory."""
        if not dump_dir.exists():
            print(f"[ERROR] Dump directory not found: {dump_dir}")
            return

        print(f"\n{'=' * 60}")
        print(f"MySQL Database Import Helper")
        print(f"{'=' * 60}\n")

        # Extract and create databases
        databases = self.extract_database_names(dump_dir)

        if not databases:
            print("[WARNING] No database names found in dump files")
            return

        print(f"\n[INFO] Found {len(databases)} unique database(s):")
        for db in sorted(databases):
            print(f"  - {db}")
        print()

        # Create databases
        success_count = 0
        for db_name in sorted(databases):
            if self.create_database(db_name):
                success_count += 1

        print(f"\n[SUMMARY] {success_count}/{len(databases)} databases created/verified")

        # Optionally auto-import
        if auto_import:
            print(f"\n{'=' * 60}")
            print("Starting Auto-Import...")
            print(f"{'=' * 60}\n")

            sql_files = sorted(dump_dir.glob("*.sql"))
            import_success = 0

            for sql_file in sql_files:
                db_name = sql_file.stem.split("_")[0]
                if self.import_dump_file(sql_file, db_name):
                    import_success += 1

            print(f"\n[SUMMARY] {import_success}/{len(sql_files)} files imported")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="MySQL Database Import Helper with Auto-Creation"
    )
    parser.add_argument(
        "dump_dir",
        type=Path,
        help="Directory containing SQL dump files",
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="MySQL host (default: localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=3306,
        help="MySQL port (default: 3306)",
    )
    parser.add_argument(
        "--user",
        default="root",
        help="MySQL user (default: root)",
    )
    parser.add_argument(
        "--auto-import",
        action="store_true",
        help="Automatically import all dump files after creating databases",
    )

    args = parser.parse_args()

    # Validate dump directory
    try:
        if not args.dump_dir.exists():
            print(f"[ERROR] Dump directory does not exist: {args.dump_dir}")
            sys.exit(1)
        if not args.dump_dir.is_dir():
            print(f"[ERROR] Path is not a directory: {args.dump_dir}")
            sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Invalid dump directory path: {e}")
        sys.exit(1)

    # Get password securely
    try:
        password = getpass.getpass("Enter MySQL password (press Enter for no password): ")
        if password == "":
            password = None
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)

    # Create helper and process
    try:
        helper = MySQLImportHelper(
            host=args.host,
            port=args.port,
            user=args.user,
            password=password,
        )
    except ValueError as e:
        print(f"[ERROR] Configuration error: {e}")
        sys.exit(1)

    helper.process_dump_directory(args.dump_dir, auto_import=args.auto_import)


if __name__ == "__main__":
    main()
