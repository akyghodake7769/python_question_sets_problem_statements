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

    idx = 1
    passed_count = 0
    failed_count = 0

    # Test Case 1: create_status_dict
    try:
        analyzer.load_scores([45, 78, 92])
        status_dict = analyzer.create_status_dict()
        expected = {45: 'Fail', 78: 'Fail', 92: 'Pass'}
        if isinstance(status_dict, dict) and status_dict == expected:
            results.append(f"✅ Test {idx}: create_status_dict – Passed")
            passed_count += 1
        else:
            results.append(f"❌ Test {idx}: create_status_dict – Failed")
            failed_count += 1
    except Exception as e:
        results.append(f"❌ Test {idx}: create_status_dict – Error: {e}")
        failed_count += 1
    idx += 1

    # Test Case 2: highest_score
    try:
        analyzer.load_scores([45, 78, 92, 55, 88, 67, 95, 52])
        highest = analyzer.highest_score()
        if highest == 95:
            results.append(f"✅ Test {idx}: highest_score – Passed")
            passed_count += 1
        else:
            results.append(f"❌ Test {idx}: highest_score – Failed")
            failed_count += 1
    except Exception as e:
        results.append(f"❌ Test {idx}: highest_score – Error: {e}")
        failed_count += 1
    idx += 1

    # Test Case 3: average_score
    try:
        analyzer.load_scores([45, 78, 92, 55, 88, 67, 95, 52])
        average = analyzer.average_score()
        expected_avg = 71.5
        if average == expected_avg:
            results.append(f"✅ Test {idx}: average_score – Passed")
            passed_count += 1
        else:
            results.append(f"❌ Test {idx}: average_score – Failed")
            failed_count += 1
    except Exception as e:
        results.append(f"❌ Test {idx}: average_score – Error: {e}")
        failed_count += 1
    idx += 1

    # Test Case 4: passing_scores_desc
    try:
        analyzer.load_scores([45, 78, 92, 55, 88, 67, 95, 52])
        passing = analyzer.passing_scores_desc()
        expected = [95, 92, 88]
        if isinstance(passing, list) and passing == expected:
            results.append(f"✅ Test {idx}: passing_scores_desc – Passed")
            passed_count += 1
        else:
            results.append(f"❌ Test {idx}: passing_scores_desc – Failed")
            failed_count += 1
    except Exception as e:
        results.append(f"❌ Test {idx}: passing_scores_desc – Error: {e}")
        failed_count += 1
    idx += 1

    # Hidden Test Case 1: All passing scores
    try:
        analyzer.load_scores([85, 90, 95, 88, 92])
        status_dict = analyzer.create_status_dict()
        expected = {85: 'Pass', 90: 'Pass', 95: 'Pass', 88: 'Pass', 92: 'Pass'}
        if isinstance(status_dict, dict) and status_dict == expected:
            results.append(f"✅ Hidden Test 1: All passing scores – Passed")
            passed_count += 1
        else:
            results.append(f"❌ Hidden Test 1: All passing scores – Failed")
            failed_count += 1
    except Exception as e:
        results.append(f"❌ Hidden Test 1: All passing scores – Error: {e}")
        failed_count += 1

    results.append(f"\n📊 Summary:")
    results.append(f"✅ Passed: {passed_count}")
    results.append(f"❌ Failed: {failed_count}\n")

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
