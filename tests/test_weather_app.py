import pytest
from unittest.mock import patch
from main import WeatherApp  # Use absolute import

class TestWeatherApp:
    
    @patch('main.requests.get')  # Update to absolute path
    def test_get_weather_data_success(self, mock_get):
        # Mock response for successful weather data retrieval
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current_weather": {
                "temperature": 25,
                "windspeed": 10,
                "winddirection": 180,
                "weathercode": 1,
            }
        }

        app = WeatherApp()
        weather_data = app.get_weather_data(60, 30)  # Example lat/lon
        assert weather_data['temperature'] == 25
        assert weather_data['wind_speed'] == 10
        assert weather_data['wind_direction'] == 180
        assert weather_data['weather_code'] == 1

    @patch('main.requests.get')  # Update to absolute path
    def test_get_coordinates_success(self, mock_get):
        # Mock response for successful coordinate retrieval
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "lat": 60,
            "lon": 30,
            "city": "Helsinki",
            "status": "success"
        }

        app = WeatherApp()
        lat, lon, city_name = app.get_coordinates()
        assert lat == 60
        assert lon == 30
        assert city_name == "Helsinki"

    @patch('main.requests.get')  # Update to absolute path
    def test_get_weather_data_failure(self, mock_get):
        # Mock response for failed weather data retrieval
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {
            "message": "City not found"
        }

        app = WeatherApp()
        weather_data = app.get_weather_data(60, 30)
        assert weather_data is None

    @patch('main.requests.get')  # Update to absolute path
    def test_get_coordinates_failure(self, mock_get):
        # Mock response for failed coordinate retrieval
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {}

        app = WeatherApp()
        lat, lon, city_name = app.get_coordinates()
        assert lat is None
        assert lon is None
        assert city_name is None
