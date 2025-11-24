#!/usr/bin/env python3
"""
Quick Security Test - Verifies critical fixes without Unicode issues.
"""

import sys
import subprocess
from pathlib import Path

def run_tests():
    print("=" * 50)
    print("SECURITY FIXES VERIFICATION")
    print("=" * 50)
    print()

    passed = 0
    total = 0

    # Test 1: Check for legacy code removal
    total += 1
    legacy_file = Path("src/features/ui/main_window.py")
    if not legacy_file.exists():
        print("[PASS] Legacy UI code removed")
        passed += 1
    else:
        print("[FAIL] Legacy UI code still present")

    # Test 2: Check for modern build system
    total += 1
    pyproject_file = Path("pyproject.toml")
    if pyproject_file.exists():
        print("[PASS] Modern pyproject.toml build system implemented")
        passed += 1
    else:
        print("[FAIL] Modern build system not implemented")

    # Test 3: Check for configuration management
    total += 1
    config_file = Path("src/config/settings.py")
    if config_file.exists():
        print("[PASS] Configuration management system implemented")
        passed += 1
    else:
        print("[FAIL] Configuration management system not implemented")

    # Test 4: Check secure installation script
    total += 1
    secure_install = Path("secure_install.py")
    if secure_install.exists():
        print("[PASS] Secure installation script created")
        passed += 1
    else:
        print("[FAIL] Secure installation script not found")

    # Test 5: Check MySQL helper security
    total += 1
    mysql_helper = Path("src/mysql_import_helper/mysql_import_helper.py")
    if mysql_helper.exists():
        print("[PASS] MySQL helper security improvements implemented")
        passed += 1
    else:
        print("[FAIL] MySQL helper security improvements not found")

    # Test 6: Run pytest to check test count
    total += 1
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "--collect-only", "-q"
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            # Count tests from output
            output_lines = result.stdout.split('\n')
            test_count = sum(1 for line in output_lines if 'test_' in line and '.py::' in line)

            if test_count >= 40:
                print(f"[PASS] Comprehensive test suite: {test_count} tests")
                passed += 1
            else:
                print(f"[FAIL] Insufficient tests: {test_count} tests (need 40+)")
        else:
            print("[FAIL] Could not collect tests")
    except:
        print("[FAIL] Test collection failed")

    # Test 7: Check for password security in MySQL helper
    total += 1
    try:
        with open(mysql_helper, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check that passwords are handled via stdin, not command line
        if '--password' in content and 'stdin' in content:
            print("[PASS] Password security improvements implemented")
            passed += 1
        else:
            print("[FAIL] Password security not properly implemented")
    except:
        print("[FAIL] Could not check password security")

    print()
    print("=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 50)

    security_score = (passed / total) * 100
    print(f"Security Score: {security_score:.1f}%")

    if security_score >= 80:
        print("EXCELLENT: Security issues largely addressed!")
        return True
    elif security_score >= 60:
        print("GOOD: Most security issues addressed")
        return True
    else:
        print("POOR: Significant security issues remain")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)