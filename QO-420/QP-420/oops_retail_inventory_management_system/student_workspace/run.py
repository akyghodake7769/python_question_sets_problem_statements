import os
import sys

def run_tests():
    # Local simple runner
    sol_path = os.path.join(os.path.dirname(__file__), "..", "secret_tests", "driver.py")
    if os.path.exists(sol_path):
        os.system(f"{sys.executable} {sol_path}")
    else:
        print("Driver not found.")

if __name__ == "__main__":
    run_tests()
