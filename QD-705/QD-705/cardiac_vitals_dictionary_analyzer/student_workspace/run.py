import importlib.util
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run.py <vm_tag> [solution_filename]")
        sys.exit(1)

    vm_tag = sys.argv[1]
    solution_filename = sys.argv[2] if len(sys.argv) > 2 else "solution.py"

    script_dir = os.path.dirname(os.path.abspath(__file__))

    solution_path = os.path.join(
        script_dir,
        "..",
        "student_workspace",
        solution_filename
    )

    driver_path = os.path.join(script_dir, "driver.py")

    spec = importlib.util.spec_from_file_location("driver", driver_path)
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)

    driver.test_student_code(solution_path, vm_tag)
