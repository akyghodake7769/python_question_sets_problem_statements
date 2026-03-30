import pandas as pd

class WeatherManager:
    """
    Data Controller responsible for loading and merging meteorological datasets.
    """
    def __init__(self):
        # TODO: Initialize df_readings and df_stations as None
        self.df_readings = None
        self.df_stations = None

    def load_data(self, readings_path: str, stations_path: str):
        """
        Reads CSV files into self.df_readings and self.df_stations.
        """
        # TODO: Load CSVs using pandas
        pass

    def get_merged_data(self) -> pd.DataFrame:
        """
        Performs an inner join on 'City'.
        """
        # TODO: Merge df_readings and df_stations
        pass

class ClimateProcessor:
    """
    Logic Processor responsible for computing meteorological metrics.
    """
    def is_heatwave(self, df: pd.DataFrame, city: str) -> bool:
        """
        Returns True if any reading for the city has Temp > 40.
        """
        # TODO: Filter by city and check Temp
        pass

    def get_rain_summary(self, df: pd.DataFrame, city: str) -> str:
        """
        Returns "Heavy Rain" if average rain > 100, "Moderate" if > 50, else "Light".
        """
        # TODO: Calculate mean for the city and return label
        pass

    def average_temp(self, df: pd.DataFrame) -> float:
        """
        Returns the overall mean temperature across all readings.
        """
        # TODO: Return mean of the Temp column
        pass

    def get_city_report(self, df: pd.DataFrame, city: str) -> dict:
        """
        Returns {'max_temp', 'min_temp', 'total_rain'} for the city.
        """
        # TODO: Aggregate metrics for the city
        pass

    def get_wettest_city(self, df: pd.DataFrame) -> str:
        """
        Returns the name of the city with the highest cumulative rainfall.
        """
        # TODO: Group by city and sum rainfall
        pass
