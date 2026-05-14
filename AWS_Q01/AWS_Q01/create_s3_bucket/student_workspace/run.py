import subprocess
import sys

def main():
    print("[SYSTEM] Initializing AWS Task Verification...")
    # This calls the verification script that checks the actual AWS resources
    result = subprocess.run([sys.executable, "verify_aws_task.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"[ERROR] {result.stderr}")

if __name__ == "__main__":
    main()
