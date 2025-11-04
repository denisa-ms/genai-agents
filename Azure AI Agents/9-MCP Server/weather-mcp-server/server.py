#!/usr/bin/env python3
"""
Weather MCP Server - Provides mock weather data through MCP protocol
"""
import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from pydantic import AnyUrl


# Mock weather data
WEATHER_CONDITIONS = [
    "Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Stormy", 
    "Snowy", "Foggy", "Windy", "Clear"
]

CITIES_DATA = {
    "New York": {"lat": 40.7128, "lon": -74.0060, "timezone": "America/New_York"},
    "London": {"lat": 51.5074, "lon": -0.1278, "timezone": "Europe/London"},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503, "timezone": "Asia/Tokyo"},
    "Paris": {"lat": 48.8566, "lon": 2.3522, "timezone": "Europe/Paris"},
    "Sydney": {"lat": -33.8688, "lon": 151.2093, "timezone": "Australia/Sydney"},
    "Dubai": {"lat": 25.2048, "lon": 55.2708, "timezone": "Asia/Dubai"},
    "Singapore": {"lat": 1.3521, "lon": 103.8198, "timezone": "Asia/Singapore"},
    "San Francisco": {"lat": 37.7749, "lon": -122.4194, "timezone": "America/Los_Angeles"},
}


def generate_mock_weather(city: str) -> dict[str, Any]:
    """Generate mock weather data for a city"""
    if city not in CITIES_DATA:
        raise ValueError(f"City '{city}' not found in database")
    
    city_info = CITIES_DATA[city]
    
    return {
        "city": city,
        "coordinates": {
            "latitude": city_info["lat"],
            "longitude": city_info["lon"]
        },
        "temperature": {
            "current": round(random.uniform(-5, 35), 1),
            "feels_like": round(random.uniform(-5, 35), 1),
            "min": round(random.uniform(-10, 25), 1),
            "max": round(random.uniform(20, 40), 1),
            "unit": "celsius"
        },
        "conditions": random.choice(WEATHER_CONDITIONS),
        "humidity": random.randint(30, 90),
        "wind": {
            "speed": round(random.uniform(0, 30), 1),
            "direction": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"]),
            "unit": "km/h"
        },
        "pressure": random.randint(990, 1030),
        "visibility": round(random.uniform(1, 10), 1),
        "uv_index": random.randint(0, 11),
        "timestamp": datetime.now().isoformat(),
        "timezone": city_info["timezone"]
    }


def generate_mock_forecast(city: str, days: int = 5) -> dict[str, Any]:
    """Generate mock weather forecast for a city"""
    if city not in CITIES_DATA:
        raise ValueError(f"City '{city}' not found in database")
    
    forecasts = []
    base_date = datetime.now()
    
    for i in range(days):
        forecast_date = base_date + timedelta(days=i)
        forecasts.append({
            "date": forecast_date.strftime("%Y-%m-%d"),
            "day_of_week": forecast_date.strftime("%A"),
            "temperature": {
                "min": round(random.uniform(-5, 20), 1),
                "max": round(random.uniform(20, 35), 1),
                "unit": "celsius"
            },
            "conditions": random.choice(WEATHER_CONDITIONS),
            "precipitation_chance": random.randint(0, 100),
            "wind_speed": round(random.uniform(5, 25), 1),
            "humidity": random.randint(40, 85)
        })
    
    return {
        "city": city,
        "forecast_days": days,
        "forecasts": forecasts,
        "generated_at": datetime.now().isoformat()
    }


def generate_mock_alerts(city: str) -> dict[str, Any]:
    """Generate mock weather alerts for a city"""
    if city not in CITIES_DATA:
        raise ValueError(f"City '{city}' not found in database")
    
    # Randomly decide if there are any alerts (30% chance)
    has_alerts = random.random() < 0.3
    
    alerts = []
    if has_alerts:
        alert_types = [
            {"type": "Heat Warning", "severity": "moderate"},
            {"type": "Storm Watch", "severity": "severe"},
            {"type": "Fog Advisory", "severity": "minor"},
            {"type": "Wind Warning", "severity": "moderate"},
            {"type": "Heavy Rain Alert", "severity": "moderate"},
        ]
        
        num_alerts = random.randint(1, 2)
        for _ in range(num_alerts):
            alert = random.choice(alert_types)
            start_time = datetime.now() + timedelta(hours=random.randint(0, 6))
            alerts.append({
                "type": alert["type"],
                "severity": alert["severity"],
                "description": f"{alert['type']} in effect for {city}",
                "start_time": start_time.isoformat(),
                "end_time": (start_time + timedelta(hours=random.randint(6, 24))).isoformat(),
                "issued_by": "Mock Weather Service"
            })
    
    return {
        "city": city,
        "alert_count": len(alerts),
        "alerts": alerts,
        "checked_at": datetime.now().isoformat()
    }


# Create the MCP server
app = Server("weather-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available weather tools"""
    return [
        Tool(
            name="get_current_weather",
            description="Get current weather conditions for a specific city. Returns temperature, conditions, humidity, wind, and other metrics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": f"City name. Available cities: {', '.join(CITIES_DATA.keys())}",
                    }
                },
                "required": ["city"],
            },
        ),
        Tool(
            name="get_weather_forecast",
            description="Get weather forecast for a specific city for the next 1-7 days. Returns daily forecasts with temperature ranges, conditions, and precipitation chances.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": f"City name. Available cities: {', '.join(CITIES_DATA.keys())}",
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to forecast (1-7)",
                        "minimum": 1,
                        "maximum": 7,
                        "default": 5,
                    },
                },
                "required": ["city"],
            },
        ),
        Tool(
            name="get_weather_alerts",
            description="Get active weather alerts and warnings for a specific city. Returns any severe weather warnings, watches, or advisories.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": f"City name. Available cities: {', '.join(CITIES_DATA.keys())}",
                    }
                },
                "required": ["city"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls for weather data"""
    
    if name == "get_current_weather":
        city = arguments.get("city")
        if not city:
            raise ValueError("city parameter is required")
        
        try:
            weather_data = generate_mock_weather(city)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(weather_data, indent=2)
                )
            ]
        except ValueError as e:
            return [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}\nAvailable cities: {', '.join(CITIES_DATA.keys())}"
                )
            ]
    
    elif name == "get_weather_forecast":
        city = arguments.get("city")
        days = arguments.get("days", 5)
        
        if not city:
            raise ValueError("city parameter is required")
        
        if days < 1 or days > 7:
            days = min(max(days, 1), 7)
        
        try:
            forecast_data = generate_mock_forecast(city, days)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(forecast_data, indent=2)
                )
            ]
        except ValueError as e:
            return [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}\nAvailable cities: {', '.join(CITIES_DATA.keys())}"
                )
            ]
    
    elif name == "get_weather_alerts":
        city = arguments.get("city")
        if not city:
            raise ValueError("city parameter is required")
        
        try:
            alerts_data = generate_mock_alerts(city)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(alerts_data, indent=2)
                )
            ]
        except ValueError as e:
            return [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}\nAvailable cities: {', '.join(CITIES_DATA.keys())}"
                )
            ]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the weather MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())