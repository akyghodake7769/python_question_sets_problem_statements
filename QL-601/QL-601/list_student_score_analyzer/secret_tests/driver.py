import importlib.util
import datetime
import os

def test_student_code(solution_path):
    # Load student solution.py dynamically
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    # Create instance of the class
    analyzer = student_module.StudentScoreAnalyzer()

    # Initialize results log
    results = []
    results.append("🧪 Running Tests for: StudentScoreAnalyzer\n")

    # Test Case 1: create_status_dict
    try:
        analyzer.load_scores([45, 78, 92])
        status_dict = analyzer.create_status_dict()
        expected = {45: 'Fail', 78: 'Fail', 92: 'Pass'}
        if isinstance(status_dict, dict) and status_dict == expected:
            results.append("✅ Visible Test Case 1 Passed: Create status dictionary")
        else:
            results.append("❌ Visible Test Case 1 Failed: Create status dictionary")
    except Exception:
        results.append("❌ Visible Test Case 1 Failed: Create status dictionary")

    # Test Case 2: highest_score
    try:
        analyzer.load_scores([45, 78, 92, 55, 88, 67, 95, 52])
        highest = analyzer.highest_score()
        if highest == 95:
            results.append("✅ Visible Test Case 2 Passed: Highest score calculation")
        else:
            results.append("❌ Visible Test Case 2 Failed: Highest score calculation")
    except Exception:
        results.append("❌ Visible Test Case 2 Failed: Highest score calculation")

    # Test Case 3: average_score
    try:
        analyzer.load_scores([45, 78, 92, 55, 88, 67, 95, 52])
        average = analyzer.average_score()
        expected_avg = 71.5
        if average == expected_avg:
            results.append("✅ Visible Test Case 3 Passed: Average score calculation")
        else:
            results.append("❌ Visible Test Case 3 Failed: Average score calculation")
    except Exception:
        results.append("❌ Visible Test Case 3 Failed: Average score calculation")

    # Test Case 4: passing_scores_desc
    try:
        analyzer.load_scores([45, 78, 92, 55, 88, 67, 95, 52])
        passing = analyzer.passing_scores_desc()
        expected = [95, 92, 88]
        if isinstance(passing, list) and passing == expected:
            results.append("✅ Visible Test Case 4 Passed: Passing scores descending")
        else:
            results.append("❌ Visible Test Case 4 Failed: Passing scores descending")
    except Exception:
        results.append("❌ Visible Test Case 4 Failed: Passing scores descending")

    # Hidden Test Case 1: All passing scores
    try:
        analyzer.load_scores([85, 90, 95, 88, 92])
        passing = analyzer.passing_scores_desc()
        expected = [95, 92, 90, 88, 85]
        if isinstance(passing, list) and passing == expected:
            results.append("✅ Hidden Test Case 1 Passed: All passing scores")
        else:
            results.append("❌ Hidden Test Case 1 Failed: All passing scores")
    except Exception:
        results.append("❌ Hidden Test Case 1 Failed: All passing scores")

    # Generate report file with timestamp
    report_folder = os.path.join(os.path.dirname(solution_path), "..", "reports")
    os.makedirs(report_folder, exist_ok=True)
    existing_reports = [f for f in os.listdir(report_folder) if f.startswith("report") and f.endswith(".txt")]
    report_filename = f"report_{len(existing_reports) + 1}.txt"
    report_path = os.path.join(report_folder, report_filename)

    with open(report_path, "w", encoding="utf-8") as f:
        for line in results:
            print(line)
            f.write(line + "\n")

    return results
