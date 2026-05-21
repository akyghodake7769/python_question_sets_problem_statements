import json
import os
import sys
import glob
from datetime import datetime, timezone, timedelta

# Capture Assessment Start Time
START_TIME_STR = os.getenv('KLOUDKRAFT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else "LOCAL_USER"

def verify_task():
    user_prefix = USER_PREFIX
    start_time = START_TIME_STR
    
    # Standard LabsKraft Header
    print("\n" + "-"*70)
    print(f"{'KODEARENA REAL-TIME JENKINS AUDIT':^70}")
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
        max_duration = 60  # 60 Min assessment

        if elapsed_minutes > max_duration + 5: # 5 min grace
            print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m")
            raise Exception("Time Limit Exceeded")

        print(f"[SYSTEM] Validating Resources for: {user_prefix}")
        print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")

        # Support both job names
        job_dir_primary = "/var/lib/jenkins/jobs/Multi-Stage-Pipeline"
        job_dir_fallback = "/var/lib/jenkins/jobs/github_jenkins_multistage_archive"
        job_dir = job_dir_primary if os.path.exists(job_dir_primary) else job_dir_fallback

        # --- TC1: GitHub Webhook & Pipeline Job Integration ---
        try:
            tc1_passed = os.path.exists(job_dir)
            if START_TIME and tc1_passed:
                mtime = datetime.fromtimestamp(os.path.getmtime(job_dir), timezone.utc)
                if mtime < (START_TIME - timedelta(minutes=30)):
                    tc1_passed = False
                    print(f"[WARN] Jenkins job was created/modified before current session started (Old Session).")

            if tc1_passed:
                results['tc1'] = True
                print(f"TC1: GitHub Webhook & Pipeline Job Integration ......... [PASSED] (10/10)")
            else:
                results['tc1'] = False
                print(f"TC1: GitHub Webhook & Pipeline Job Integration ......... [FAILED] (0/10)")
                print(f"     └─ [Reason]: Webhook trigger not configured or activated in current session.")
        except Exception as e:
            results['tc1'] = False
            print(f"TC1: GitHub Webhook & Pipeline Job Integration ......... [FAILED] (0/10)")
            print(f"     └─ [Error]: {str(e)}")

        # --- TC2: Multi-Stage Execution ---
        if not results.get('tc1'):
            results['tc2'] = False
            print(f"TC2: Multi-Stage Execution Check (Lint & Build) ........ [FAILED] (0/10)")
            print(f"     └─ [Reason]: Prerequisite failed (Job does not exist).")
            results['tc3'] = False
            print(f"TC3: Jenkins Artifact Archiving Verification ........... [FAILED] (0/10)")
            print(f"     └─ [Reason]: Prerequisite failed.")
        else:
            try:
                builds_path = f"{job_dir}/builds"
                all_builds = glob.glob(f"{builds_path}/[0-9]*") if os.path.exists(builds_path) else []
                build_dir_stable = f"{job_dir}/builds/lastStableBuild"
                build_dir_successful = f"{job_dir}/builds/lastSuccessfulBuild"
                
                # Check for any successful build
                tc2_passed = os.path.exists(build_dir_stable) or os.path.exists(build_dir_successful)
                
                if START_TIME and tc2_passed:
                    mtime = datetime.fromtimestamp(os.path.getmtime(build_dir_stable if os.path.exists(build_dir_stable) else build_dir_successful), timezone.utc)
                    if mtime < (START_TIME - timedelta(minutes=30)):
                        tc2_passed = False
                        print(f"[WARN] Jenkins build was completed before current session started (Old Session).")

                if tc2_passed:
                    results['tc2'] = True
                    print(f"TC2: Multi-Stage Execution Check (Lint & Build) ........ [PASSED] (10/10)")
                else:
                    results['tc2'] = False
                    print(f"TC2: Multi-Stage Execution Check (Lint & Build) ........ [FAILED] (0/10)")
                    
                    # Enhanced Diagnostics
                    if len(all_builds) == 0:
                        print(f"     └─ [Reason]: No builds found! The Webhook did NOT trigger Jenkins, or you haven't run a build yet.")
                    else:
                        print(f"     └─ [Reason]: Builds exist, but NONE were successful. Your Jenkinsfile likely has an error! Check the Jenkins Console Output.")
            except Exception as e:
                results['tc2'] = False
                print(f"TC2: Multi-Stage Execution Check (Lint & Build) ........ [FAILED] (0/10)")
                print(f"     └─ [Error]: {str(e)}")
            
            # --- TC3: Artifact Archiving ---
            try:
                archive_dir_stable = f"{job_dir}/builds/lastStableBuild/archive"
                archive_dir_success = f"{job_dir}/builds/lastSuccessfulBuild/archive"
                
                archive_dir = archive_dir_stable if os.path.exists(archive_dir_stable) else archive_dir_success
                
                tc3_passed = os.path.exists(archive_dir) and len(os.listdir(archive_dir)) > 0
                
                if START_TIME and tc3_passed:
                    mtime = datetime.fromtimestamp(os.path.getmtime(archive_dir), timezone.utc)
                    if mtime < (START_TIME - timedelta(minutes=30)):
                        tc3_passed = False

                if tc3_passed:
                    results['tc3'] = True
                    print(f"TC3: Jenkins Artifact Archiving Verification ........... [PASSED] (10/10)")
                else:
                    results['tc3'] = False
                    print(f"TC3: Jenkins Artifact Archiving Verification ........... [FAILED] (0/10)")
                    if not results.get('tc2'):
                        print(f"     └─ [Reason]: Prerequisite failed (No successful build found).")
                    else:
                        print(f"     └─ [Reason]: Build was successful, but NO artifacts were found. Check your archiveArtifacts directive.")
            except Exception as e:
                results['tc3'] = False
                print(f"TC3: Jenkins Artifact Archiving Verification ........... [FAILED] (0/10)")
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
