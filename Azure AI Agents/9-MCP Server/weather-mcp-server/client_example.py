#!/usr/bin/env python3
"""
Example client for the Weather MCP Server
Demonstrates how to connect to and use the weather MCP server
"""
import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Main function to demonstrate MCP client usage"""
    
    # Define server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )
    
    print("🌤️  Weather MCP Client Example")
    print("=" * 50)
    print()
    
    # Connect to the MCP server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Initialize the session
            await session.initialize()
            print("✓ Connected to Weather MCP Server")
            print()
            
            # List available tools
            tools_result = await session.list_tools()
            print(f"📋 Available Tools ({len(tools_result.tools)}):")
            for tool in tools_result.tools:
                print(f"  • {tool.name}: {tool.description}")
            print()
            
            # Example 1: Get current weather
            print("=" * 50)
            print("Example 1: Get Current Weather for New York")
            print("=" * 50)
            
            result = await session.call_tool(
                "get_current_weather",
                arguments={"city": "New York"}
            )
            
            weather_data = json.loads(result.content[0].text)
            print(f"🌡️  Temperature: {weather_data['temperature']['current']}°C")
            print(f"🌤️  Conditions: {weather_data['conditions']}")
            print(f"💧 Humidity: {weather_data['humidity']}%")
            print(f"💨 Wind: {weather_data['wind']['speed']} {weather_data['wind']['unit']} {weather_data['wind']['direction']}")
            print(f"🌅 UV Index: {weather_data['uv_index']}")
            print()
            
            # Example 2: Get weather forecast
            print("=" * 50)
            print("Example 2: Get 3-Day Forecast for London")
            print("=" * 50)
            
            result = await session.call_tool(
                "get_weather_forecast",
                arguments={"city": "London", "days": 3}
            )
            
            forecast_data = json.loads(result.content[0].text)
            print(f"📅 {forecast_data['forecast_days']}-Day Forecast:")
            for day in forecast_data['forecasts']:
                print(f"\n  {day['day_of_week']} ({day['date']}):")
                print(f"    Temperature: {day['temperature']['min']}°C - {day['temperature']['max']}°C")
                print(f"    Conditions: {day['conditions']}")
                print(f"    Precipitation: {day['precipitation_chance']}%")
            print()
            
            # Example 3: Get weather alerts
            print("=" * 50)
            print("Example 3: Get Weather Alerts for Tokyo")
            print("=" * 50)
            
            result = await session.call_tool(
                "get_weather_alerts",
                arguments={"city": "Tokyo"}
            )
            
            alerts_data = json.loads(result.content[0].text)
            if alerts_data['alert_count'] > 0:
                print(f"⚠️  Active Alerts: {alerts_data['alert_count']}")
                for alert in alerts_data['alerts']:
                    print(f"\n  • {alert['type']} ({alert['severity'].upper()})")
                    print(f"    {alert['description']}")
                    print(f"    Valid: {alert['start_time']} to {alert['end_time']}")
            else:
                print("✓ No active weather alerts")
            print()
            
            # Example 4: Demonstrate error handling
            print("=" * 50)
            print("Example 4: Error Handling (Invalid City)")
            print("=" * 50)
            
            try:
                result = await session.call_tool(
                    "get_current_weather",
                    arguments={"city": "InvalidCity"}
                )
                print(result.content[0].text)
            except Exception as e:
                print(f"Error occurred: {e}")
            print()
            
            print("=" * 50)
            print("✓ All examples completed successfully!")
            print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())