import subprocess
import os

def setup_git_repo():
    ws = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(["git", "init"], cwd=ws, capture_output=True)
    subprocess.run(["git", "config", "user.name", "dev_alice"], cwd=ws, capture_output=True)
    subprocess.run(["git", "config", "user.email", "alice@company.com"], cwd=ws, capture_output=True)
    
    outage_log = os.path.join(ws, "outage_trace.log")
    with open(outage_log, "w", encoding="utf-8") as f:
        f.write("2026-08-06 10:00:00 [CRITICAL] Database connection pool exhausted by commit 8c9e012. Exception: ConnectionTimeoutException at Pool.java:98\n")
    subprocess.run(["git", "add", "."], cwd=ws, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Hotfix: outage trace log baseline"], cwd=ws, capture_output=True)
    print("[SUCCESS] Outage RCA Git repo initialized!")

if __name__ == "__main__":
    setup_git_repo()
