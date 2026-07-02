import json
import os
import sys

def verify_task_central(username, start_time_str):
    print(f"\n--- Central Validation for {username} ---")
    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace', 'solution.json'))
    try:
        with open(ws_path, 'r') as f:
            data = json.load(f)
            score = data.get('score', 0)
            print(f"Score retrieved: {score}/20")
            return score, data.get('results', {})
    except Exception as e:
        print("Failed to read local verification results.")
        return 0, {}
