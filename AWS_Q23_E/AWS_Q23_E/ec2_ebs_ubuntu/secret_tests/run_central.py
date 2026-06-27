import subprocess
import sys
import os

def main():
    print("[SYSTEM] Initializing Central AWS Task Verification (Q23)...")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.normpath(os.path.join(current_dir, "driver_central.py"))

    if not os.path.exists(driver_path):
        print(f"[ERROR] Central driver not found at: {driver_path}")
        return

    args = [sys.executable, driver_path]
    if len(sys.argv) > 1:
        args.append(sys.argv[1])

    subprocess.run(args, capture_output=False, text=True)

if __name__ == "__main__":
    main()
