# Weather MCP Server

A Model Context Protocol (MCP) server that provides mock weather data for demonstration purposes. This server exposes three weather-related APIs through the MCP protocol.

## Features

### Available Tools

1. **get_current_weather** - Get current weather conditions for a specific city
   - Returns: temperature, conditions, humidity, wind speed/direction, pressure, visibility, UV index

2. **get_weather_forecast** - Get weather forecast for 1-7 days
   - Returns: daily forecasts with temperature ranges, conditions, precipitation chances

3. **get_weather_alerts** - Get active weather alerts and warnings
   - Returns: severe weather warnings, watches, or advisories

### Supported Cities

- New York
- London
- Tokyo
- Paris
- Sydney
- Dubai
- Singapore
- San Francisco

## Installation

1. **Clone or download this repository**

2. **Install dependencies:**

```bash
cd weather-mcp-server

```

## Usage

### Running the Server

The server uses stdio transport and is designed to be run by an MCP client:

```bash
python server.py
```

### Using the Client Example

A complete example client is provided to demonstrate how to interact with the server:

```bash
python client_example.py
```

The client example demonstrates:
- Connecting to the MCP server
- Listing available tools
- Getting current weather data
- Fetching weather forecasts
- Checking weather alerts
- Error handling for invalid cities

### Example Output

```
🌤️  Weather MCP Client Example
==================================================

✓ Connected to Weather MCP Server

📋 Available Tools (3):
  • get_current_weather: Get current weather conditions for a specific city...
  • get_weather_forecast: Get weather forecast for a specific city...
  • get_weather_alerts: Get active weather alerts and warnings...

==================================================
Example 1: Get Current Weather for New York
==================================================
🌡️  Temperature: 22.3°C
🌤️  Conditions: Partly Cloudy
💧 Humidity: 65%
💨 Wind: 15.2 km/h NW
🌅 UV Index: 7
```

## API Reference

### get_current_weather

**Parameters:**
- `city` (string, required): Name of the city

**Returns:** JSON object with:
```json
{
  "city": "New York",
  "coordinates": {
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "temperature": {
    "current": 22.3,
    "feels_like": 21.5,
    "min": 18.0,
    "max": 26.0,
    "unit": "celsius"
  },
  "conditions": "Partly Cloudy",
  "humidity": 65,
  "wind": {
    "speed": 15.2,
    "direction": "NW",
    "unit": "km/h"
  },
  "pressure": 1013,
  "visibility": 8.5,
  "uv_index": 7,
  "timestamp": "2024-01-15T14:30:00",
  "timezone": "America/New_York"
}
```

### get_weather_forecast

**Parameters:**
- `city` (string, required): Name of the city
- `days` (integer, optional): Number of days (1-7, default: 5)

**Returns:** JSON object with:
```json
{
  "city": "London",
  "forecast_days": 3,
  "forecasts": [
    {
      "date": "2024-01-15",
      "day_of_week": "Monday",
      "temperature": {
        "min": 12.0,
        "max": 18.5,
        "unit": "celsius"
      },
      "conditions": "Rainy",
      "precipitation_chance": 75,
      "wind_speed": 18.5,
      "humidity": 80
    }
  ],
  "generated_at": "2024-01-15T14:30:00"
}
```

### get_weather_alerts

**Parameters:**
- `city` (string, required): Name of the city

**Returns:** JSON object with:
```json
{
  "city": "Tokyo",
  "alert_count": 1,
  "alerts": [
    {
      "type": "Storm Watch",
      "severity": "severe",
      "description": "Storm Watch in effect for Tokyo",
      "start_time": "2024-01-15T16:00:00",
      "end_time": "2024-01-16T08:00:00",
      "issued_by": "Mock Weather Service"
    }
  ],
  "checked_at": "2024-01-15T14:30:00"
}
```

## Integration with MCP Clients

To integrate this server with MCP-compatible applications, configure it in your MCP settings:

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["path/to/weather-mcp-server/server.py"]
    }
  }
}
```

## Development

### Project Structure

```
weather-mcp-server/
├── server.py           # Main MCP server implementation
├── client_example.py   # Example client demonstrating usage
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Mock Data

The server generates random mock data for demonstration purposes. Each request returns different random values within realistic ranges:

- **Temperature:** -5°C to 35°C
- **Humidity:** 30% to 90%
- **Wind Speed:** 0 to 30 km/h
- **UV Index:** 0 to 11
- **Weather Conditions:** Sunny, Partly Cloudy, Cloudy, Rainy, Stormy, Snowy, Foggy, Windy, Clear

### Extending the Server

To add more cities, update the `CITIES_DATA` dictionary in [`server.py`](server.py:21):

```python
CITIES_DATA = {
    "Your City": {"lat": 0.0, "lon": 0.0, "timezone": "Your/Timezone"},
    # ... existing cities
}
```

To add new tools, use the `@app.tool()` decorator and implement the corresponding handler in the `call_tool` function.

## Requirements

- Python 3.8+
- mcp >= 1.0.0
- pydantic >= 2.0.0

## License

This is a demonstration project. Feel free to use and modify as needed.

## Notes

⚠️ **Important:** This server provides MOCK data only. Do not use for actual weather information. For real weather data, integrate with a proper weather API service like OpenWeatherMap, Weather.com, or similar.