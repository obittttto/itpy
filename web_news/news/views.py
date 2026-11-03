from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Article

from django.shortcuts import render, get_object_or_404, redirect
from .forms import ArticleForm


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

def category(request, category_name=None):
    if category_name is None:
        articles = Article.objects.filter(
            is_published=True
        ).order_by("-created_at")

        category_name = "Все категории"
    else:
        articles = Article.objects.filter(
            is_published=True,
            category__iexact=category_name,
        ).order_by("-created_at")

    context = {
        "articles": articles,
        "category_name": category_name,
    }

    return render(
        request,
        "news/category.html",
        context,
    )

def article_detail(request, article_id):
    article = get_object_or_404(
        Article,
        id=article_id,
        is_published=True,
    )

    context = {
        "article": article,
    }

    return render(
        request,
        "news/article_detail.html",
        context,
    )

# def edit_article(request, article_id):
#     article = get_object_or_404(
#         Article,
#         id=article_id
#     )
#
#     if request.method == "POST":
#         form = ArticleForm(
#             request.POST,
#             request.FILES,
#             instance=article
#         )
#
#         if form.is_valid():
#             article = form.save()
#
#             if article.is_published:
#                 return redirect(
#                     "article_detail",
#                     article_id=article.id
#                 )
#
#             return redirect("home")
#
#     else:
#         form = ArticleForm(instance=article)
#
#     context = {
#         "form": form,
#         "article": article,
#     }
#
#     return render(
#         request,
#         "news/edit_article.html",
#         context
#     )

def test_form(request):
    context = {}

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        context = {
            "title": title,
            "content": content,
        }

    return render(
        request,
        "news/test_form.html",
        context,
    )
def add_article(request):

    if request.method == "POST":

        form = ArticleForm(request.POST)

        if form.is_valid():

            article = form.save()

            return redirect(
                "article_detail",
                article_id=article.id,
            )

    else:
        form = ArticleForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "news/add_article.html",
        context,
    )
# Create your views here.
