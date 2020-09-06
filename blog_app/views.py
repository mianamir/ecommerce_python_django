from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

def home(request):
    posts = Post.objects.all()
    context = { 'posts': posts }
    return render(request, 'blog_app/home.html', context)


def about_us(request):
    return render(request, 'blog_app/about.html', {'title': 'About'})