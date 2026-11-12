from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Article
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ArticleForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required

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
        is_published=True,
        is_active=True
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
    article = Article.objects.get(id=article_id)

    context = {
        "article": article,
    }

    return render(
        request,
        "news/article_detail.html",
        context,
    )


@login_required
@permission_required("news.change_article", raise_exception=True)
def edit_article(request, article_id):
    article = get_object_or_404(
        Article,
        id=article_id
    )

    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            request.FILES,
            instance=article
        )

        if form.is_valid():
            article = form.save()

            if article.is_published:
                return redirect(
                    "article_detail",
                    article_id=article.id
                )

            return redirect("home")

    else:
        form = ArticleForm(instance=article)

    context = {
        "form": form,
        "article": article,
    }

    return render(
        request,
        "news/edit_article.html",
        context
    )


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

@login_required
@permission_required("news.add_article", raise_exception=True)
def article_created(request):
    return render(
        request,
        "news/article_created.html",
    )



@login_required
@permission_required("news.delete_article", raise_exception=True)
def delete_article(request, article_id):
    article = get_object_or_404(
        Article,
        id=article_id
    )

    if request.method == "POST":
        article.delete()
        return redirect("home")

    context = {
        "article": article,
    }

    return render(
        request,
        "news/delete_article.html",
        context
    )

@login_required
@permission_required("news.change_article", raise_exception=True)
def archive_article(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id,
        is_active=True
    )

    if request.method == "POST":

        article.is_active = False

        article.save(
            update_fields=["is_active"]
        )

        return redirect("home")

    return render(
        request,
        "news/archive_article.html",
        {"article": article}
    )

@login_required
@permission_required("news.change_article", raise_exception=True)
def restore_article(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id,
        is_active=False
    )

    if request.method == "POST":

        article.is_active = True

        article.save(
            update_fields=["is_active"]
        )

        return redirect("home")

    return render(
        request,
        "news/restore_article.html",
        {"article": article}
    )

# Create your views here.
