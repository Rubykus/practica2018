# from django.shortcuts import render
import requests
import datetime
import pytz

from django.shortcuts import render
from django.conf import settings

from .forms import WeatherForm
from .models import Weather
from .helpers import round_date, get_intervaks_count, get_all_dates


def index(req):
    form = WeatherForm()

    return render(req, 'index.html', {'form': form})


def weather(req):
    if req.method == 'POST':
        form = WeatherForm(req.POST)

        if form.is_valid():
            storage = 'DB'
            city_name = form.cleaned_data['city'].lower()

            current_date = round_date(datetime.datetime.utcnow().replace(tzinfo=pytz.utc))
            from_date = round_date(form.cleaned_data['from_date'])
            to_date = round_date(form.cleaned_data['to_date'])

            Weather.objects.filter(city_name__exact=city_name, date__lt=current_date).delete()
            weathers = Weather.objects.filter(city_name__exact=city_name, date__range=(from_date, to_date)).order_by('date')

            count = get_intervaks_count(to_date - from_date)

            if (weathers.count() == count):
                return render(req, 'weather.html', {'weathers': weathers, 'from': storage, 'city': city_name})

            all_dates = get_all_dates(from_date, to_date)
            exist_dates = [w.date for w in weathers]
            dates = [d for d in all_dates if d not in exist_dates]

            api_url = 'https://api.openweathermap.org/data/2.5/forecast'
            res = requests.get(api_url, params={'q': city_name, 'APPID': settings.APPID})

            if res.status_code == 200:
                storage = 'API'
                data = res.json()['list']

                for w in data:
                    date = datetime.datetime.fromtimestamp(w['dt']).replace(tzinfo=pytz.utc)
                    if date in dates:
                        weather = Weather()
                        weather.city_name = city_name
                        weather.temp = w['main']['temp']
                        weather.pressure = w['main']['pressure']
                        weather.wind_speed = w['wind']['speed']
                        weather.date = date
                        weather.save()
            else:
                error = 'City \'{}\' was not found'.format(city_name)
                return render(req, 'error.html', {'error': error})

            return render(req, 'weather.html', {'weathers': weathers.all(), 'from': storage, 'city': city_name})

        else:
            return render(req, 'error.html', {'error': 'Dates are invalid'})

    return render(req, 'error.html', {'error': 'Unknow method'})
