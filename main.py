from weather_api import get_weather
city=input("Enter location(City, Country): ")
result=get_weather(city)

if result["success"]:
    print(f"\nWeather in {city}:")
    print(f"Temperature: {result['temp_c']}°C / {result['temp_f']}°F")
    print(f"Humidity: {result['humidity']}%")
    print(f"Cloud cover: {result['cloud']}%")
    print(f"Condition: {result['description']}")
else:
    print(f"\nError: {result['message']}")