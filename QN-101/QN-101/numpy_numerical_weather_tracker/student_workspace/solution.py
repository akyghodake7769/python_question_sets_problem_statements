import numpy as np

class WeatherTracker:
    """
    Numerical Weather Data Management System using NumPy.
    Manages weather data with efficient numerical computations.
    """

    def __init__(self):
        """
        Initialize the WeatherTracker.
        Create storage for temperature, precipitation, and wind speed data.
        """
        self.temperatures = np.array([])
        self.precipitation = np.array([])
        self.wind_speed = np.array([])

    def add_temperature_data(self, temps: list) -> np.ndarray:
        """
        Add temperature data to the tracker.
        
        Parameters:
            temps (list): List of temperature values
        
        Returns:
            np.ndarray: The stored temperature array
        """
        self.temperatures = np.array(temps)
        return self.temperatures

    def calculate_average_temperature(self) -> float:
        """
        Calculate the average temperature from stored data.
        
        Returns:
            float: Average temperature (2 decimal places), or 0.0 if no data exists
        """
        if len(self.temperatures) == 0:
            return 0.0
        return round(float(np.mean(self.temperatures)), 2)

    def get_days_above_temperature(self, threshold: float) -> np.ndarray:
        """
        Get all temperature readings above a threshold.
        
        Parameters:
            threshold (float): Temperature threshold value
        
        Returns:
            np.ndarray: Array of temperatures greater than threshold
        """
        return self.temperatures[self.temperatures > threshold]

    def get_weather_statistics(self) -> dict:
        """
        Get comprehensive weather statistics.
        
        Returns:
            dict: Contains 'min_temp', 'max_temp', 'avg_temp', 'data_points'
                  All numeric values rounded to 2 decimals
                  Returns zeros if no data
        """
        if len(self.temperatures) == 0:
            return {
                'min_temp': 0.0,
                'max_temp': 0.0,
                'avg_temp': 0.0,
                'data_points': 0
            }
        
        return {
            'min_temp': round(float(np.min(self.temperatures)), 2),
            'max_temp': round(float(np.max(self.temperatures)), 2),
            'avg_temp': round(float(np.mean(self.temperatures)), 2),
            'data_points': len(self.temperatures)
        }
