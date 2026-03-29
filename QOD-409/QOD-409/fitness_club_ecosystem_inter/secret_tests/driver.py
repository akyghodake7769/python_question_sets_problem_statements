import importlib.util
import os
import sys
import random

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable. Make sure it's a method."
    return True, None

# Embedded Reference Logic for Grading (Oracle)
class _GradingLogic:
    @staticmethod
    def calc_fee(tier, sessions):
        base = {'Standard': 40.0, 'Premium': 80.0, 'VIP': 150.0}.get(tier, 0.0)
        return float(base + sessions * 20.0)

    @staticmethod
    def calc_stats(total, attended):
        rate = round((attended / total * 100), 2) if total > 0 else 0.0
        return {'total_sessions': total, 'attendance_rate': rate}

# Helper for Test Setups (Ultimate Independence - Force Internal State)
def _setup_member(reg, name, tier, solution):
    if not hasattr(reg, 'members'): reg.members = {}
    prof = solution.MemberProfile(name, tier)
    prof.name = name; prof.tier = tier; prof.session_logs = []
    reg.members[name] = prof
    return reg

def _setup_session(reg, name, d, t, tier="Standard", solution=None):
    if not hasattr(reg, 'members'): reg.members = {}
    prof = solution.MemberProfile(name, tier)
    prof.name = name; prof.tier = tier; prof.session_logs = [{'date': d, 'time': t, 'trainer': 'Trainer_X', 'attended': False}]
    reg.members[name] = prof
    return reg

def _setup_multi_sessions(reg, name, tier, solution):
    if not hasattr(reg, 'members'): reg.members = {}
    prof = solution.MemberProfile(name, tier)
    prof.name = name; prof.tier = tier; prof.session_logs = []
    num = random.randint(1, 5)
    for i in range(num):
        prof.session_logs.append({'date': f"2026-04-{i+1}", 'time': "12:00", 'trainer': f"T{i}", 'attended': False})
    reg.members[name] = prof
    return reg, {'tier': tier, 'sessions': num}

def _setup_random_attendance(reg, name, solution):
    if not hasattr(reg, 'members'): reg.members = {}
    tier = random.choice(['Standard', 'Premium', 'VIP'])
    prof = solution.MemberProfile(name, tier)
    prof.name = name; prof.tier = tier; prof.session_logs = []
    total = random.randint(2, 6)
    attended = random.randint(1, total)
    for i in range(total):
        att_flag = (i < attended)
        prof.session_logs.append({'date': f"2026-05-{i+1}", 'time': "10:00", 'trainer': f"T{i}", 'attended': att_flag})
    reg.members[name] = prof
    return reg, {'total': total, 'attended': attended}

def test_student_code(solution_path):
    report_dir = os.path.dirname(solution_path)
    report_path = os.path.join(report_dir, "report.txt")
    
    # Load Student Solution
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        msg = f"IMPORT ERROR: {e}"
        print(msg)
        with open(report_path, "w", encoding="utf-8") as f: f.write(msg + "\n")
        return

    header = "Running Tests for: Smart Fitness Club Ecosystem (Internal) - Log Optimized\n"
    print(header)
    report_lines = [header]

    if not hasattr(solution, "ClubRegistry"):
        msg = "ERROR: ClubRegistry class not found in solution.py"
        print(msg); report_lines.append(msg)
        with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")
        return

    # Randomized Context for Hardcoding Prevention
    random.seed(None)
    rv = random.randint(100, 999); member_name = f"Member_{rv}"
    date_str = f"2026-03-{random.randint(10, 28)}"
    random_tier = random.choice(['Standard', 'Premium', 'VIP'])

    test_cases = [
        {
            "desc": "Verification of registry initialization",
            "func": "__init__",
            "setup": lambda: solution.ClubRegistry(),
            "call": lambda obj: obj.members,
            "check": lambda res: isinstance(res, dict) and len(res) == 0,
            "expected_output": "ClubRegistry.members should be an empty dictionary.",
            "marks": 0
        },
        {
            "desc": "Registering a valid profile",
            "func": "add_member",
            "setup": lambda: solution.ClubRegistry(),
            "call": lambda obj: (obj.add_member(member_name, "Standard"), member_name in obj.members if hasattr(obj, 'members') else False),
            "check": lambda res: res == (True, True),
            "expected_output": f"Member '{member_name}' added to dictionary.",
            "marks": 1
        },
        {
            "desc": "Verification of tiered zone access",
            "func": "can_access_zone",
            "setup": lambda: _setup_member(solution.ClubRegistry(), member_name, "Premium", solution),
            "call": lambda obj: (obj.can_access_zone(member_name, "Pool"), obj.can_access_zone(member_name, "Private_Studio")),
            "check": lambda res: res == (True, False),
            "expected_output": "Premium access: Pool=True, Studio=False.",
            "marks": 1
        },
        {
            "desc": "Scheduling unique workout slots",
            "func": "schedule_session",
            "setup": lambda: _setup_member(solution.ClubRegistry(), member_name, random_tier, solution),
            "call": lambda obj: (obj.schedule_session(member_name, date_str, "10:00", "Trainer_A"), obj.schedule_session(member_name, date_str, "10:00", "Trainer_B")),
            "check": lambda res: res == (True, False),
            "expected_output": "Conflict check: Second session at same time returns False.",
            "marks": 1
        },
        {
            "desc": "Membership tier upgrade logic",
            "func": "upgrade_tier",
            "setup": lambda: _setup_member(solution.ClubRegistry(), member_name, "Standard", solution),
            "call": lambda obj: (obj.upgrade_tier(member_name, "VIP"), obj.members[member_name].tier),
            "check": lambda res: res == (True, "VIP"),
            "expected_output": "Tier upgraded from Standard to VIP.",
            "marks": 1
        },
        {
            "desc": "Logging attendance record",
            "func": "mark_attendance",
            "setup": lambda: _setup_session(solution.ClubRegistry(), member_name, date_str, "14:00", tier=random_tier, solution=solution),
            "call": lambda obj: (obj.mark_attendance(member_name, date_str, "14:00"), any(s['attended'] for s in obj.members[member_name].session_logs if s['date'] == date_str)),
            "check": lambda res: res == (True, True),
            "expected_output": "Attendance flag flipped to True.",
            "marks": 1
        },
        {
            "desc": "Membership + trainer fees calculation",
            "func": "get_monthly_fee",
            "setup": lambda: _setup_multi_sessions(solution.ClubRegistry(), member_name, random_tier, solution),
            "call": lambda obj: obj.get_monthly_fee(member_name),
            "check": lambda res, ctx: abs(float(res) - _GradingLogic.calc_fee(ctx['tier'], ctx['sessions'])) < 0.01,
            "expected_output": "Expected fee (Base + Session Fees) dynamically calculated.",
            "marks": 2.5
        },
        {
            "desc": "Member engagement analytics",
            "func": "get_member_stats",
            "setup": lambda: _setup_random_attendance(solution.ClubRegistry(), member_name, solution),
            "call": lambda obj: obj.get_member_stats(member_name),
            "check": lambda res, ctx: res == _GradingLogic.calc_stats(ctx['total'], ctx['attended']),
            "expected_output": "Analytics match dynamic session count and attendance rate.",
            "marks": 2.5
        }
    ]

    total_score = 0
    for idx, case in enumerate(test_cases, 1):
        marks = case["marks"]
        try:
            # Handle possible context from setup
            setup_res = case["setup"]()
            if isinstance(setup_res, tuple):
                obj, context = setup_res
            else:
                obj, context = setup_res, None
            
            # Universal Force State for Registry (AttributeError Prevention for logic-related tests ONLY)
            if idx > 1 and not hasattr(obj, 'members'): setattr(obj, 'members', {})

            valid, err = validate_method_exists(obj, case["func"])
            if not valid:
                msg = f"FAIL TC{idx} [{case['desc']}]: {err}"
                print(msg); report_lines.append(msg); continue

            result = case["call"](obj)
            
            # Dynamic check call
            if context:
                passed = case["check"](result, context)
            else:
                passed = case["check"](result)

            if passed:
                total_score += float(marks)
                msg = f"PASS TC{idx} [{case['desc']}] ({marks}/{marks})"
            else:
                msg = f"FAIL TC{idx} [{case['desc']}] (0/{marks})\n  Expected: {case['expected_output']}"
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}] (0/{marks}) | Error: {type(e).__name__}: {e}"
        print(msg); report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/10.0"
    print(score_line); report_lines.append(score_line)
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
