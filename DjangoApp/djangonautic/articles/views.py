from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from . import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


def article_list(request):
    articles = Article.objects.all().order_by('-date');
    return render(request, 'articles/article_list.html', { 'articles': articles })

def article_detail(request, slug):
    instance = Article.objects.get(slug=slug)
    return render(request, "articles/article_detail.html", {'instance': instance})

@login_required(login_url="/accounts/login/")
def article_create(request):
    quote = "Create an Awesome New Article"
    button = "Create"
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            # save article to db
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    return render(request, 'articles/article_create.html', { 'form': form, 'quote': quote, 'b' : button })

def article_update(request, slug):
    if not request.user.is_authenticated:
        raise Http404
    instance = Article.objects.get(slug=slug)
    if not instance.author_id == request.user.id:
        raise Http404
    quote = "Update Blog"
    button="Update and Save"
    form = forms.CreateArticle(request.POST or None,request.FILES or None,instance=instance)
    duplicate = Article.objects.get(id=instance.id)
    duplicate.delete()
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        instance.author = request.user
        return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    return render(request, 'articles/article_create.html', { 'form': form, 'quote': quote, 'b' : button })

def article_delete(request,slug):
    if not request.user.is_authenticated:
        raise Http404
    instance = Article.objects.get(slug=slug)
    if not instance.author_id == request.user.id:
        raise Http404
    instance.delete()
    articles = Article.objects.all().order_by('-date');
    return render(request, 'articles/article_list.html', { 'articles': articles })

def add_comment_to_post(request, slug):
    article = Article.objects.get(slug=slug)
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.post = article
            instance.save()
            return redirect('articles:detail', slug=instance.post.slug)
    else:
        form = forms.CommentForm()
    return render(request, 'articles/add_comment_to_post.html', {'form': form})
