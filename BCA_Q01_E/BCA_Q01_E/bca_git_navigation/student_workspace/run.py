import subprocess
import sys
import os

def unpack_bundle_if_needed():
    ws = os.path.dirname(os.path.abspath(__file__))
    dot_git = os.path.join(ws, ".git")
    bundle = os.path.join(ws, "repo.bundle")
    
    # If .git is missing or empty but repo.bundle exists, unpack it
    res = subprocess.run(["git", "log", "-n", "1"], cwd=ws, capture_output=True, text=True)
    if (res.returncode != 0 or "fatal" in res.stderr.lower()) and os.path.exists(bundle):
        print("[SYSTEM] Unpacking Git history from repo.bundle...")
        subprocess.run(["git", "clone", "repo.bundle", ".git_temp"], cwd=ws, capture_output=True)
        temp_dot_git = os.path.join(ws, ".git_temp", ".git")
        if os.path.exists(temp_dot_git):
            import shutil
            if os.path.exists(dot_git):
                shutil.rmtree(dot_git, ignore_errors=True)
            shutil.move(temp_dot_git, dot_git)
            shutil.rmtree(os.path.join(ws, ".git_temp"), ignore_errors=True)
            print("[SYSTEM] Git repository history successfully restored!")

def main():
    unpack_bundle_if_needed()
    print("[SYSTEM] Running local tests...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.normpath(os.path.join(current_dir, "..", "secret_tests", "driver.py"))
    if not os.path.exists(driver_path):
        print(f"[ERROR] Driver not found at: {driver_path}")
        sys.exit(1)
    
    result = subprocess.run([sys.executable, driver_path], capture_output=False, text=True)
    sys.exit(result.returncode)

if __name__ == "__main__":
    unpack_bundle_if_needed()
    main()
