import pandas as pd


class DeliveryAnalyzer:
    """Analyze warehouse delivery performance and status tracking."""

    def create_delivery_df(self, delivery_data: list) -> pd.DataFrame:
        """
        Create a structured delivery DataFrame from raw list data.
        
        Args:
            delivery_data: List of [DeliveryID, Warehouse, Date, Status]
        
        Returns:
            DataFrame with columns: DeliveryID, Warehouse, Date, Status
        """
        df = pd.DataFrame(delivery_data, columns=["DeliveryID", "Warehouse", "Date", "Status"])
        return df

    def compute_monthly_delivery_rate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute monthly delivery success rate per warehouse.
        
        Args:
            df: Delivery DataFrame
        
        Returns:
            DataFrame with Warehouse, Month, and Delivery Rate columns
            Delivery Rate = (Delivered count / Total count) * 100
        """
        df = df.copy()
        # Extract month (YYYY-MM)
        df["Month"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m")
        
        # Count total deliveries per warehouse per month
        total_counts = df.groupby(["Warehouse", "Month"]).size().reset_index(name="Total")
        
        # Count delivered records per warehouse per month
        delivered_df = df[df["Status"] == "Delivered"]
        delivered_counts = delivered_df.groupby(["Warehouse", "Month"]).size().reset_index(name="Delivered")
        
        # Merge and calculate rate
        result = total_counts.merge(delivered_counts, on=["Warehouse", "Month"], how="left").fillna(0)
        result["Delivery Rate"] = (result["Delivered"] / result["Total"] * 100).round(1)
        result = result[["Warehouse", "Month", "Delivery Rate"]]
        
        return result

    def add_delay_flag(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add a binary flag for delayed deliveries.
        
        Args:
            df: Delivery DataFrame
        
        Returns:
            DataFrame with added IsDelayed column (1 or 0)
        """
        df = df.copy()
        df["IsDelayed"] = (df["Status"] == "Delayed").astype(int)
        return df

    def high_returns(self, df: pd.DataFrame, threshold: int) -> pd.DataFrame:
        """
        Identify warehouses with frequent product returns.
        
        Args:
            df: Delivery DataFrame
            threshold: Minimum count of returns to include
        
        Returns:
            DataFrame with Warehouse and Return Count columns for warehouses exceeding threshold
        """
        returned_df = df[df["Status"] == "Returned"]
        return_counts = returned_df.groupby("Warehouse").size().reset_index(name="Return Count")
        result = return_counts[return_counts["Return Count"] > threshold]
        return result

    def warehouse_status_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a summary of delivery statuses per warehouse.
        
        Args:
            df: Delivery DataFrame
        
        Returns:
            DataFrame with Warehouse and status columns (Delivered, Delayed, Returned counts)
        """
        status_counts = df.groupby(["Warehouse", "Status"]).size().unstack(fill_value=0)
        result = status_counts.reset_index()
        return result

    def clean_delivery_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove invalid or incomplete delivery records.
        
        Args:
            df: Delivery DataFrame
        
        Returns:
            Cleaned DataFrame with invalid statuses and null values removed
        """
        df = df.copy()
        valid_statuses = ["Delivered", "Delayed", "Returned"]
        df = df[df["Status"].isin(valid_statuses)]
        df = df.dropna(subset=["Status"])
        return df
