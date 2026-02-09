import pandas as pd

class ClaimsAnalyzer:

    def create_claims_df(self, claim_data: list) -> pd.DataFrame:
        return pd.DataFrame(claim_data, columns=["CustomerID", "Category", "Amount", "Status", "Date"])

    def approval_rate_by_category(self, df: pd.DataFrame) -> pd.DataFrame:
        grouped = df.groupby("Category")
        total_claims = grouped.size().reset_index(name="Total")
        approved_claims = df[df["Status"] == "Approved"].groupby("Category").size().reset_index(name="Approved")
        result = total_claims.merge(approved_claims, on="Category", how="left")
        result["Approved"] = result["Approved"].fillna(0).astype(int)
        result["Approval Rate"] = (result["Approved"] / result["Total"] * 100).round(1)
        return result[["Category", "Approval Rate"]]

    def add_flag_high_amount(self, df: pd.DataFrame, threshold: float) -> pd.DataFrame:
        result = df.copy()
        result["IsHighValue"] = (result["Amount"] > threshold).astype(int)
        return result

    def get_top_pending_claims(self, df: pd.DataFrame, n: int) -> pd.DataFrame:
        pending = df[df["Status"] == "Pending"]
        return pending.sort_values(by="Amount", ascending=False).head(n).reset_index(drop=True)

    def claim_summary_by_status(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.groupby("Status")["Amount"].agg(
            TotalAmount="sum",
            MinAmount="min",
            MaxAmount="max",
            AvgAmount="mean"
        ).reset_index()
        result["AvgAmount"] = result["AvgAmount"].round(2)
        return result

    def clean_invalid_claims(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df[
            (df["Status"].isin(["Approved", "Rejected", "Pending"])) &
            (df["Amount"].notna()) &
            (df["Amount"] > 0)
        ]
        return result.reset_index(drop=True)
