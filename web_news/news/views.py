from django.http import HttpResponse
from django.shortcuts import render
from .models import Article


# def index(request):
#     return HttpResponse("Главная страница новостей")


def about(request):
    content = {
        "title": "О нашем новостном издании",
        "text":
            "«Минский вестник» — независимое городское новостное интернет-издание, основанное в 2018 году. "
            "Издание специализируется на оперативной информации о жизни города, развитии инфраструктуры, "
            "культурных событиях и расследованиях локального масштаба. Аудитория портала превышает 150 000 "
            "читателей ежемесячно. Миссия редакции — честный и объективный рассказ о событиях столицы "
            "без «воды» и кликбейта."
        ,

    }
    return render(request, "news/about.html", content)

def contact(request):
    content = {
        "title": "Наши контакты",
        "contacts": [
            "Email: info@gmail.com",
            "Телефон: +375 29 123-45-67",
            "Адрес: г. Минск, ул. Октябрьская, д.11",
        ],
    }
    return render(request, 'news/contact.html', content)

def index(request):
    articles = Article.objects.filter(
        is_published=True
    ).order_by("-created_at")

    context = {
        "articles": articles,
    }

    return render(
        request,
        "news/index.html",
        context,
    )

def category(request):
    content = {
        "category_name": "Технологии",
        "articles": [
            "Представлена новая модель смартфона",
            "Компания выпустила обновление программного обеспечения",
            "Учёные разработали новый процессор",
        ],
    }
    return render(request, "news/category.html", content)


# Create your views here.
