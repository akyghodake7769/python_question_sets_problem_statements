import os
from test_cases.test_config import run_tests

if __name__ == "__main__":
    if os.path.exists("test_report.log"):
        os.remove("test_report.log")
    results = run_tests()
    with open("test_report.log", "w") as f:
        for line in results:
            f.write(line + "\n")
    print("\nSummary written to test_report.log")
