from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Главная страница новостей")


def about(request):
    return HttpResponse("О нашем новостном издании")

# Create your views here.
