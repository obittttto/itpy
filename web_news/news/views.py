from django.http import HttpResponse
from django.shortcuts import render


# def index(request):
#     return HttpResponse("Главная страница новостей")


# def about(request):
#     return HttpResponse("О нашем новостном издании")


def index(request):
    return render(request, "news/index.html")

# Create your views here.
