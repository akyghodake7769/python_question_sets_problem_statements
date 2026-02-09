import pandas as pd

class GymUsageAnalyzer:

    def create_usage_df(self, logs: list) -> pd.DataFrame:
        return pd.DataFrame(logs, columns=["Member", "Branch", "Workout", "Duration"])

    def compute_total_duration(self, usage_df: pd.DataFrame) -> pd.DataFrame:
        result = usage_df.groupby("Member")["Duration"].sum().reset_index()
        result.rename(columns={"Duration": "Total Duration"}, inplace=True)
        return result

    def add_calorie_column(self, usage_df: pd.DataFrame) -> pd.DataFrame:
        df = usage_df.copy()
        # Define burn rates
        rates = {"Cardio": 8, "Weights": 7, "Yoga": 5}
        # Map workout type to burn rate; default to 6 if not found
        df["Rate"] = df["Workout"].map(rates).fillna(6)
        df["Calories Burned"] = (df["Duration"] * df["Rate"]).astype(int)
        return df.drop(columns=["Rate"])

    def filter_long_sessions(self, usage_df: pd.DataFrame, min_minutes: int) -> pd.DataFrame:
        return usage_df[usage_df["Duration"] >= min_minutes].reset_index(drop=True)

    def get_top_sessions(self, usage_df: pd.DataFrame, n: int) -> pd.DataFrame:
        return usage_df.sort_values(by="Calories Burned", ascending=False).head(n)
    
    def remove_duplicates(self, usage_df: pd.DataFrame) -> pd.DataFrame:
        return usage_df.drop_duplicates().reset_index(drop=True)
