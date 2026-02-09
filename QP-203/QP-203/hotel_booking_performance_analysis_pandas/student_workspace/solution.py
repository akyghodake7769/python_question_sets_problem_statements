import pandas as pd


class HotelBookingAnalyzer:
    """Analyze hotel booking logs for performance insights."""

    def create_booking_df(self, booking_data: list) -> pd.DataFrame:
        """
        Create a structured booking DataFrame from raw list data.
        
        Args:
            booking_data: List of [Guest, Hotel, Date, Status, Amount]
        
        Returns:
            DataFrame with columns: Guest, Hotel, Date, Status, Amount
        """
        df = pd.DataFrame(booking_data, columns=["Guest", "Hotel", "Date", "Status", "Amount"])
        return df

    def compute_monthly_revenue(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute monthly revenue per hotel from booked reservations.
        
        Args:
            df: Booking DataFrame
        
        Returns:
            DataFrame with Hotel, Month, and Revenue columns
        """
        df = df.copy()
        # Filter only booked records
        booked_df = df[df["Status"] == "Booked"]
        
        # Extract month (YYYY-MM)
        booked_df = booked_df.copy()
        booked_df["Month"] = pd.to_datetime(booked_df["Date"]).dt.strftime("%Y-%m")
        
        # Group by Hotel and Month, sum Amount
        result = booked_df.groupby(["Hotel", "Month"])["Amount"].sum().reset_index()
        result.columns = ["Hotel", "Month", "Revenue"]
        return result

    def add_cancellation_flag(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add a binary flag for cancelled bookings.
        
        Args:
            df: Booking DataFrame
        
        Returns:
            DataFrame with added IsCancelled column (1 or 0)
        """
        df = df.copy()
        df["IsCancelled"] = (df["Status"] == "Cancelled").astype(int)
        return df

    def get_no_show_guests(self, df: pd.DataFrame, threshold: int) -> pd.DataFrame:
        """
        Identify guests with frequent no-show records.
        
        Args:
            df: Booking DataFrame
            threshold: Minimum count of no-shows to include
        
        Returns:
            DataFrame with Guest and NoShowCount columns for guests exceeding threshold
        """
        no_show_df = df[df["Status"] == "No-show"]
        guest_counts = no_show_df.groupby("Guest").size().reset_index(name="NoShowCount")
        result = guest_counts[guest_counts["NoShowCount"] > threshold]
        return result

    def hotel_status_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a summary of booking statuses per hotel.
        
        Args:
            df: Booking DataFrame
        
        Returns:
            DataFrame with Hotel and status columns (Booked, Cancelled, No-show counts)
        """
        status_counts = df.groupby(["Hotel", "Status"]).size().unstack(fill_value=0)
        result = status_counts.reset_index()
        return result

    def clean_booking_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove invalid or incomplete booking records.
        
        Args:
            df: Booking DataFrame
        
        Returns:
            Cleaned DataFrame with invalid statuses and null amounts removed
        """
        df = df.copy()
        valid_statuses = ["Booked", "Cancelled", "No-show"]
        df = df[df["Status"].isin(valid_statuses)]
        df = df.dropna(subset=["Amount"])
        return df
