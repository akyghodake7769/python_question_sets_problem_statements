#!/usr/bin/env python3
"""
E-Commerce Order Analyzer - Test Runner
"""

import os
import sys

# Add secret_tests directory to path for imports
secret_tests_path = os.path.join(os.path.dirname(__file__), '..', 'secret_tests')
sys.path.insert(0, secret_tests_path)

from driver import test_student_code

if __name__ == "__main__":
    solution_path = os.path.join(os.path.dirname(__file__), 'solution.py')
    test_student_code(solution_path)
