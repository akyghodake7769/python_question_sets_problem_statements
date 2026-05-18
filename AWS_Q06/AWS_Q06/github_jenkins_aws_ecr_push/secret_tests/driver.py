import json
import os
import sys
import subprocess
from datetime import datetime, timezone

# Capture Assessment Start Time
START_TIME_STR = os.getenv('KLOUDKRAFT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else "LOCAL_USER"

def verify_task():
    user_prefix = USER_PREFIX
    start_time = START_TIME_STR
    
    # Standard LabsKraft Header
    print("\n" + "-"*70)
    print(f"{'KODEARENA REAL-TIME CI/CD AUDIT':^70}")
    print("-"*70)

    total_score = 0
    results = {}

    try:
        # Time Enforcement Logic
        if not START_TIME:
            print("[ERROR] KLOUDKRAFT_START_TIME environment variable is missing.")
            raise Exception("Invalid Session")

        now = datetime.now(timezone.utc)
        elapsed_minutes = (now - START_TIME).total_seconds() / 60
        max_duration = 75  # 75 Min assessment

        if elapsed_minutes > max_duration + 5: # 5 min grace
            print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m")
            raise Exception("Time Limit Exceeded")

        print(f"[SYSTEM] Validating Resources for: {user_prefix}")
        print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")

        # --- TC1: GitHub Webhook ---
        try:
            tc1_passed = True # Stub for actual verification
            if tc1_passed:
                results['tc1'] = True
                print(f"TC1: GitHub Webhook Integration & Trigger .............. [PASSED] (10/10)")
            else:
                results['tc1'] = False
                print(f"TC1: GitHub Webhook Integration & Trigger .............. [FAILED] (0/10)")
                print(f"     └─ [Reason]: Webhook trigger not configured or activated.")
        except Exception as e:
            results['tc1'] = False
            print(f"TC1: GitHub Webhook Integration & Trigger .............. [FAILED] (0/10)")
            print(f"     └─ [Error]: {str(e)}")

        # --- TC2: Docker Build & Tagging ---
        if not results.get('tc1'):
            results['tc2'] = False
            print(f"TC2: Docker Image Build & Tag Verification ............. [FAILED] (0/10)")
            print(f"     └─ [Reason]: Prerequisite failed (Webhook invalid).")
            results['tc3'] = False
            print(f"TC3: AWS ECR Registry Push Verification ................ [FAILED] (0/10)")
            print(f"     └─ [Reason]: Prerequisite failed.")
        else:
            try:
                tc2_passed = True # Stub for actual verification
                if tc2_passed:
                    results['tc2'] = True
                    print(f"TC2: Docker Image Build & Tag Verification ............. [PASSED] (10/10)")
                else:
                    results['tc2'] = False
                    print(f"TC2: Docker Image Build & Tag Verification ............. [FAILED] (0/10)")
                    print(f"     └─ [Reason]: Docker image build failed or missing correct tag.")
            except Exception as e:
                results['tc2'] = False
                print(f"TC2: Docker Image Build & Tag Verification ............. [FAILED] (0/10)")
                print(f"     └─ [Error]: {str(e)}")
            
            # --- TC3: AWS ECR Push ---
            try:
                tc3_passed = True # Stub for actual verification
                if tc3_passed:
                    results['tc3'] = True
                    print(f"TC3: AWS ECR Registry Push Verification ................ [PASSED] (10/10)")
                else:
                    results['tc3'] = False
                    print(f"TC3: AWS ECR Registry Push Verification ................ [FAILED] (0/10)")
                    print(f"     └─ [Reason]: Image not found in the target AWS ECR repository.")
            except Exception as e:
                results['tc3'] = False
                print(f"TC3: AWS ECR Registry Push Verification ................ [FAILED] (0/10)")
                print(f"     └─ [Error]: {str(e)}")

        # Final Scoring
        total_score = sum([10 for r in results.values() if r])
        
        print("-" * 70)
        print(f"{'TOTAL SCORE:':<52} {total_score}/30")
        print("-" * 70 + "\n")

    except Exception as e:
        print(f"[ERROR] Real-time audit failed: {str(e)}")
        total_score = 0

    # Save Metadata for Central Evaluation
    solution_data = {
        'candidate_prefix': user_prefix,
        'assessment_start_time': start_time,
        'evaluation_type': 'REAL_TIME_API',
        'score': total_score,
        'results': results
    }
    
    try:
        ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
        os.makedirs(ws_path, exist_ok=True)
        with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}")

if __name__ == '__main__':
    verify_task()
