#!/usr/bin/env python3
"""
Local Test Runner for Event Manager
Run: python run.py
"""

import os
import sys

# Add the secret_tests directory to the path
secret_tests_dir = os.path.join(os.path.dirname(__file__), "..", "secret_tests")
sys.path.insert(0, secret_tests_dir)

from driver import test_student_code

if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "solution.py")
    test_student_code(solution_file)
