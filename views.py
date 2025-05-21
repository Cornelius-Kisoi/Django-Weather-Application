from django.shortcuts import render
import requests
from datetime import datetime

def weather(request):
    data = {}
    if request.method == 'POST':
        city = request.POST.get('city')
        unit = request.POST.get('unit', 'metric')  # default to Celsius

        units_param = 'metric' if unit == 'metric' else 'imperial'
        temp_symbol = '°C' if unit == 'metric' else '°F'

        source = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units_param}&appid=4049262e57f517b3b0f46e8670349fa5"
        response = requests.get(source)
        list_data = response.json()

        if response.status_code == 200 and 'sys' in list_data:
            weather_info = list_data.get("weather", [{}])[0]
            sunrise = datetime.fromtimestamp(list_data['sys'].get('sunrise')).strftime('%H:%M:%S')
            sunset = datetime.fromtimestamp(list_data['sys'].get('sunset')).strftime('%H:%M:%S')

            data = {
                "country_code": list_data['sys'].get('country', 'N/A'),
                "coordinates": f"{list_data['coord']['lon']}, {list_data['coord']['lat']}",
                "temp": round(list_data['main']['temp'], 1),
                "humidity": list_data['main']['humidity'],
                "description": weather_info.get("description", "N/A").capitalize(),
                "icon": weather_info.get("icon", ""),
                "wind": list_data['wind'].get('speed', 'N/A'),
                "sunrise": sunrise,
                "sunset": sunset,
                "temp_symbol": temp_symbol,
                "lat": list_data['coord']['lat'],
                "lon": list_data['coord']['lon'],
                "unit": unit,
                "error": None
            }
        else:
            data = {"error": f"City '{city}' not found or invalid response."}
    return render(request, 'weather.html', data)



# from django.shortcuts import render, HttpResponse
# import json
# import requests

# # Create your views here.
# def weather(request):
#     if request.method == 'POST':
#         city = request.POST['city']
#         source = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=4049262e57f517b3b0f46e8670349fa5"
#         list_data = requests.get(source.format(city)).json()

#         data = {
#             "country_code": str(list_data["sys"]['country']),
#             "coordinates": str(list_data['coord']['lon']) + ' ' + str(list_data['coord']['lat']),
#             "temp": round((list_data['main']['temp']-32)*5.0/9.0,2),
#             "humidity": str(list_data['main']['humidity'])
#         }
#     else:
#         data = {}
#     return render(request, 'weather.html', data)