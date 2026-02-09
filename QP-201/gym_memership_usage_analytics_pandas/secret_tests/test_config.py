import pandas as pd
from student import GymUsageAnalyzer

def run_tests():
    analyzer = GymUsageAnalyzer()
    results = []

    def log_result(name, passed, reason="", visibility="visible"):
        status = "[PASS]" if passed else f"[FAIL - {reason}]"
        results.append(f"{status} {name} ({visibility})")
        print(results[-1])

    try:
        df = analyzer.create_usage_df([["Alice", "Downtown", "Cardio", 45]])
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["Member", "Branch", "Workout", "Duration"]
        assert df.shape[0] == 1
        log_result("create_usage_df", True)
    except Exception as e:
        log_result("create_usage_df", False, str(e))

    try:
        df = pd.DataFrame({
            "Member": ["Alice", "Alice", "Bob"],
            "Branch": ["D", "D", "U"],
            "Workout": ["Cardio", "Yoga", "Weights"],
            "Duration": [45, 30, 60]
        })
        out = analyzer.compute_total_duration(df)
        assert "Total Duration" in out.columns
        assert out[out["Member"] == "Alice"]["Total Duration"].iloc[0] == 75
        log_result("compute_total_duration", True)
    except Exception as e:
        log_result("compute_total_duration", False, str(e))

    try:
        df = pd.DataFrame({
            "Member": ["Alice", "Bob"],
            "Branch": ["D", "U"],
            "Workout": ["Cardio", "Weights"],
            "Duration": [45, 60]
        })
        res = analyzer.add_calorie_column(df)
        assert "Calories Burned" in res.columns
        assert res.loc[res["Workout"] == "Cardio", "Calories Burned"].iloc[0] == 360
        log_result("add_calorie_column", True)
    except Exception as e:
        log_result("add_calorie_column", False, str(e))

    try:
        df = pd.DataFrame({
            "Member": ["Alice", "Bob"],
            "Branch": ["D", "U"],
            "Workout": ["Cardio", "Weights"],
            "Duration": [30, 60]
        })
        res = analyzer.filter_long_sessions(df, 45)
        assert res.shape[0] == 1
        assert res["Member"].iloc[0] == "Bob"
        log_result("filter_long_sessions", True)
    except Exception as e:
        log_result("filter_long_sessions", False, str(e))

    try:
        df = pd.DataFrame({
            "Member": ["Alice", "Bob", "Zoe"],
            "Branch": ["A", "B", "C"],
            "Workout": ["Yoga", "Cardio", "Weights"],
            "Duration": [30, 60, 45]
        })
        df["Calories Burned"] = [150, 480, 315]
        res = analyzer.get_top_sessions(df, 2)
        assert res.iloc[0]["Calories Burned"] >= res.iloc[1]["Calories Burned"]
        log_result("get_top_sessions", True)
    except Exception as e:
        log_result("get_top_sessions", False, str(e))

    # Hidden Tests
    try:
        df = pd.DataFrame([
            ["Zoe", "D", "Yoga", 30],
            ["Zoe", "D", "Yoga", 30]
        ], columns=["Member", "Branch", "Workout", "Duration"])
        res = analyzer.remove_duplicates(df)
        assert res.shape[0] == 1
        log_result("remove_duplicates", True, visibility="hidden")
    except Exception as e:
        log_result("remove_duplicates", False, str(e), visibility="hidden")

    try:
        df = pd.DataFrame([
            ["Alice", "D", "Cardio", 0]
        ], columns=["Member", "Branch", "Workout", "Duration"])
        res = analyzer.compute_total_duration(df)
        assert res["Total Duration"].iloc[0] == 0
        log_result("compute_total_duration_zero", True, visibility="hidden")
    except Exception as e:
        log_result("compute_total_duration_zero", False, str(e), visibility="hidden")

    try:
        df = pd.DataFrame([
            ["Bob", "U", "Weights", 45],
            ["Eve", "U", "Weights", 45]
        ], columns=["Member", "Branch", "Workout", "Duration"])
        df["Calories Burned"] = [315, 315]
        res = analyzer.get_top_sessions(df, 1)
        assert res["Calories Burned"].iloc[0] == 315
        log_result("get_top_sessions_tie", True, visibility="hidden")
    except Exception as e:
        log_result("get_top_sessions_tie", False, str(e), visibility="hidden")

    return results
