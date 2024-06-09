from django.shortcuts import render
import json
import requests
from .models import City, Worldcities
import datetime
from django.contrib import messages
# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=762966bee22ea724acb4d3cdc562f3aa'

    city = request.POST.get('city')

    cities = Worldcities.objects.order_by('field1')

    try:
        city_weather = requests.get(url.format(city)).json()
    except requests.exceptions.RequestException as e:
        # Handle potential API request errors
        messages.error(request, f"An error occurred while fetching weather data: {e}")
        return render(request, 'error.html', {'message': 'API request error'})

    if 'cod' not in city_weather or city_weather['cod'] != 200:  # Check for API error code
        # City not found or other API error
        return render(request, 'error.html', {'message': 'City not found'})

    celcius_weather = (city_weather['main']['temp'] - 32) * 5/9
    high = (city_weather['main']['temp_max'] - 32) * 5/9
    low = (city_weather['main']['temp_min'] - 32) * 5/9

    date_time = datetime.datetime.fromtimestamp(city_weather['dt'])

    weather = {
        'city': city,
        'temperature': celcius_weather,
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon'],
        'humidity': city_weather['main']['humidity'],
        'pressure': city_weather['main']['pressure'],
        'wind': city_weather['wind']['speed'],
        'feels_like': (city_weather['main']['feels_like'] - 32) * 5/9,
        'date': date_time,
        'percipitation': city_weather['main']['feels_like'],
        'high': high,
        'low': low,
    }

    weather_icons = {
        '01d' : 'wi-day-sunny.png',
        '01n' : 'wi-night-clear.png',
        '02d' : 'wi-day-cloudy.png',
        '02n' : 'wi-night-alt-cloudy.png',
        '03d' : 'wi-cloud.png',
        '03n' : 'wi-cloud.png',
        '04d' : 'wi-cloudy.png',
        '04n' : 'wi-cloudy.png',
        '09d' : 'wi-showers.png',
        '09n' : 'wi-showers.png',
        '10d' : 'wi-day-showers.png',
        '10n' : 'wi-night-alt-showers.png',
        '11d' : 'wi-thunderstorm.png',
        '11n' : 'wi-thunderstorm.png',
        '13d' : 'wi-snow.png',
        '13n' : 'wi-snow.png',
        '50d' : 'wi-fog.png',
        '50n' : 'wi-fog.png',
    }

    context = {
        'cities': cities,
        'weather': weather,
        'weather_icons': weather_icons,
    }

    return render(request, 'index.html', context)