from dotenv import load_dotenv
import streamlit as st
import requests

load_dotenv()


class WeatherApp:
    def __init__(self):
        # Open-Meteo does not require an API key
        pass

    def get_weather_data(self, lat, lon):
        """Fetch weather data for the given latitude and longitude using Open-Meteo API."""
        base_url = "https://api.open-meteo.com/v1/forecast"
        complete_url = f"{base_url}?latitude={lat}&longitude={lon}&current_weather=true"

        # Fetch the data from Open-Meteo API
        response = requests.get(complete_url)
        data = response.json()

        # Check for a successful response
        if response.status_code == 200:
            # Extract relevant data safely
            current = data.get('current_weather', {})
            temperature = current.get('temperature', "N/A")
            wind_speed = current.get('windspeed', "N/A")
            wind_direction = current.get('winddirection', "N/A")
            weather_code = current.get('weathercode', "N/A")

            city_weather = {
                'temperature': temperature,
                'wind_speed': wind_speed,
                'wind_direction': wind_direction,
                'weather_code': weather_code
            }
            return city_weather
        else:
            st.error(data.get("message", "Failed to retrieve data"))
            return None

    def get_coordinates(self):
        """Fetch latitude and longitude from an external API."""
        # Fetch the user's IP-based location
        response = requests.get("http://ip-api.com/json/")
        data = response.json()

        if response.status_code == 200 and data.get("status") == "success":
            return data["lat"], data["lon"], data["city"]
        else:
            st.error("Failed to fetch current location.")
            return None, None, None

    def render_weather(self, weather_data, city_name):
        """Render the weather information in the Streamlit interface."""
        if weather_data:
            # Center the temperature with large font size
            st.markdown(
                f"<h1 style='text-align: center; font-size: 64px;'>The weather in {city_name}</h1>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<h1 style='text-align: center; font-size: 64px;'>{weather_data['temperature']}°C</h1>",
                unsafe_allow_html=True
            )
            st.write(f"**Wind Speed**: {weather_data['wind_speed']} km/h")
            st.write(
                f"**Wind Direction**: {weather_data['wind_direction']}° "
                f"<span title='The direction from which the wind is blowing. "
                f"0° is North, 90° is East, 180° is South, and 270° is West.' "
                f"style='color: blue; cursor: help;'>[?]</span>",
                unsafe_allow_html=True
            )
            st.write(
                f"**Weather Code**: {weather_data['weather_code']} "
                f"<span title='Weather codes represent current weather conditions. "
                f"Refer to the documentation for more details.' "
                f"style='color: blue; cursor: help;'>[?]</span>",
                unsafe_allow_html=True
            )
        else:
            st.error("Weather data not found!")

    def run(self):
        """Main method to run the Streamlit weather app."""
        st.set_page_config(layout="centered")  # Center the content
        st.title("Weather App 🌤️")

        # Get latitude, longitude, and city from the external API
        lat, lon, city_name = self.get_coordinates()

        # Fetch weather data for the coordinates if they are available
        if lat and lon:  # Ensure that both latitude and longitude are provided
            weather_data = self.get_weather_data(lat, lon)

            # Render weather data on the interface
            self.render_weather(weather_data, city_name)


# Main entry point
if __name__ == "__main__":
    app = WeatherApp()
    app.run()
