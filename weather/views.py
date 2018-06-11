# from django.shortcuts import render
from django.shortcuts import render

from .forms import CityForm


def index(request):
    form = CityForm()

    return render(request, 'index.html', {'form': form})


def weather(request):
    return render(request, 'weather.html', {'city': request.POST['city']})
