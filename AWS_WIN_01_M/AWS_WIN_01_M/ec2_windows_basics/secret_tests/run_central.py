import os
import sys
import json
import traceback

try:
    from driver_central import verify_aws_on_server
except ImportError:
    from driver import verify_aws_on_server

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 run_central.py <vm_tag> <solution_filename> [exam_code]")
        sys.exit(1)

    vm_tag = sys.argv[1]
    solution_filename = sys.argv[2]
    solution_path = os.path.abspath(solution_filename)

    print("\n🚀 Starting DevOps AWS Windows Basics Central Evaluation...")
    print(f"📌 VM Tag       : {vm_tag}")
    print(f"📄 Solution file: {solution_filename}")
    print(f"📂 Full path    : {solution_path}")

    if not os.path.exists(solution_path):
        print(f"❌ Solution file not found at: {solution_path}")
        sys.exit(1)

    try:
        with open(solution_path, 'r') as f:
            data = json.load(f)
            candidate_email = data.get('candidate_email') or data.get('email') or vm_tag
            labskraft_user = data.get('candidate_prefix') or data.get('labskraft_username')
            start_time = data.get('assessment_start_time')
            
            # The central server passes exam_code as the 3rd argument (sys.argv[3]) if available
            exam_code = sys.argv[3] if len(sys.argv) > 3 else "UNKNOWN"
            
            verify_aws_on_server(candidate_email, data.get('question_id', 'AWS_WIN_01_M'), labskraft_user, start_time, solution_data=data, exam_code=exam_code)
        
        print("✅ Central Evaluation finished successfully.")
    except Exception as e:
        print(f"❌ An error occurred during evaluation: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
