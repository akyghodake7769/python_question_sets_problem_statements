import sys
import os

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except Exception:
    script_dir = os.getcwd()

if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from driver import test_student_code

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run.py <vm_tag> [solution_filename] [exam_code]")
        sys.exit(1)
        
    vm_tag = sys.argv[1]
    solution_filename = sys.argv[2] if len(sys.argv) > 2 else os.path.join(script_dir, "../student_workspace/solution.py")
    exam_code = sys.argv[3] if len(sys.argv) > 3 else "UNKNOWN_EXAM"
    solution_path = os.path.abspath(solution_filename)

    test_student_code(solution_path=solution_path, vm_tag=vm_tag, exam_code=exam_code)
