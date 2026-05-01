from enum import Enum
from typing import Dict, Any, Optional
import sys

# Complete the 'WeatherService' class below.
#
# Processes weather queries using a dynamic Enum.

class WeatherService:
    # Class-level variable to store the dynamic Enum
    WeatherData: Optional[Enum] = None

    @staticmethod
    def initialize_data(data: Dict[str, Dict[str, Any]]) -> None:
        """Dynamically creates an Enum from city data."""
        # Implementation here
        pass

    @staticmethod
    def get_temperature(city: str) -> str:
        """Fetches temperature for a given city from the dynamic Enum."""
        # Implementation here (including range validation -25 to 122)
        return ""

    @staticmethod
    def get_forecast(city: str) -> str:
        """Fetches forecast for a given city from the dynamic Enum."""
        # Implementation here
        return ""

def process_weather_queries():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
        
    line_idx = 0
    n_cities = int(input_data[line_idx].strip())
    line_idx += 1
    city_map = {}
    
    for _ in range(n_cities):
        if line_idx >= len(input_data): break
        line = input_data[line_idx].strip().split(",")
        city = line[0].strip()
        temp = line[1].strip()
        forecast = line[2].strip()
        city_map[city] = {"temp": temp, "forecast": forecast}
        line_idx += 1
    
    WeatherService.initialize_data(city_map)

    if line_idx >= len(input_data): return
    n_queries = int(input_data[line_idx].strip())
    line_idx += 1
    
    for _ in range(n_queries):
        if line_idx >= len(input_data): break
        query = input_data[line_idx].strip().split(",")
        line_idx += 1
        if len(query) < 2: continue
        city = query[0].strip()
        q_type = query[1].strip()
        
        if q_type == "temperature":
            print(WeatherService.get_temperature(city))
        elif q_type == "forecast":
            print(WeatherService.get_forecast(city))

if __name__ == '__main__':
    process_weather_queries()
