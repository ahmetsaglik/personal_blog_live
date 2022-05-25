from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from blog.models import BlogPost, Category
from blog.forms import CreateBlogPostForm
from django.urls import reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


POSTS_PER_PAGE = 10

def must_authenticate_view(request):
    context = {}
    return render(request, 'snippets/must_authenticate.html', context)


def home_page_view(request):
    context = {}
    posts = BlogPost.objects.all()

    context['posts'] = posts

    return render(request, 'index.html', context)


def about_page_view(request):
    context = {}

    return render(request, 'about.html', context)


def create_blog_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must-authenticate')
    
    if request.POST:
        form = CreateBlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            author = user
            obj.author = author
            obj.save()
            return redirect('home')
    else:
        form = CreateBlogPostForm()
              
    context['form'] = form
    return render(request, 'create_post.html', context)


def detail_post_view(request, slug):
    context = {}
    
    if not request.user.is_authenticated:
        return redirect('must-authenticate')

    blog_post = get_object_or_404(BlogPost, slug=slug)

    context['blog_post'] = blog_post
    

    return render(request, 'blog-post.html', context)


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = BlogPost.objects.filter(
            Q(title__icontains=q),
            Q(body__icontains=q),
        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))


def all_categories_view(request):
    context = {}

    categories = Category.objects.all()

    context['categories'] = categories
    return render(request, 'blog_category_list.html', context)


def show_category_page_view(request, category_name):
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    posts = BlogPost.objects.all().filter(category__name = category_name)
    
    # Pagination
    page = request.GET.get('page', 1)
    posts_paginator = Paginator(posts, POSTS_PER_PAGE)

    try:
        posts = posts_paginator.page(page)
    except PageNotAnInteger:
        posts = posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        posts = posts_paginator.page(posts_paginator.num_pages)

    context['posts'] = posts
    context['category_name'] = category_name

    return render(request, 'category_page.html', context)















































