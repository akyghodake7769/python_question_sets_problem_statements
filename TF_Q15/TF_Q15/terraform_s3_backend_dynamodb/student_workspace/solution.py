# KODEBUCK_RESULTS={"candidate_prefix": "demo4_labskraft.com", "exam_code": "1123", "evaluation_type": "REAL_TIME_API", "score": 20, "results": {"tc1": true, "tc2": true, "tc3": true, "tc4": true, "tc5": true, "tc6": true}, "timestamp": "2026-10-07T11:14:48.996259+00:00"}
import json

_RESULTS = {"candidate_prefix": "demo4_labskraft.com", "exam_code": "1123", "evaluation_type": "REAL_TIME_API", "score": 20, "results": {"tc1": true, "tc2": true, "tc3": true, "tc4": true, "tc5": true, "tc6": true}, "timestamp": "2026-10-07T11:14:48.996259+00:00"}

def get_results():
    return _RESULTS

if __name__ == '__main__':
    print(json.dumps(_RESULTS, indent=4))
