import sys
import importlib.util
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_central.py <vm_tag> [solution_filename]")
        sys.exit(1)
    
    vm_tag = sys.argv[1]
    solution_filename = sys.argv[2] if len(sys.argv) > 2 else "solution.py"
    
    # Construct the solution path
    solution_path = os.path.join("/home/ubuntu/submissions", solution_filename)
    
    # Load and execute driver_central
    driver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "driver_central.py"))
    spec = importlib.util.spec_from_file_location("driver_central", driver_path)
    driver_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver_module)
    
    driver_module.test_student_code(solution_path, vm_tag)


if __name__ == "__main__":
    main()
