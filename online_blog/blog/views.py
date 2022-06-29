from blog.forms import PostForm, ReviewForm
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Post, Tag

# Create your views here.


def home(request):
    return render(request, "main.html")


def posts(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    posts = Post.objects.filter(title__icontains=search_query)
    context = {"posts": posts}
    return render(request, "blog/posts.html", context)


def post(request, pk):
    post = Post.objects.get(id=pk)
    tags = post.tags.all()
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project_id = post
        review.profile_id = request.user.profile
        review.save()

    context = {
        "post": post,
        "tags": tags,
        "form": form,
    }

    return render(request, "blog/single_post.html", context)


@user_passes_test(lambda user: user.is_autor, login_url="posts")
@login_required(login_url="login")
def create_post(request):
    form = PostForm()
    profile = request.user.profile

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.autor_id = profile.user.autor
            project.save()
            return redirect("posts")

    context = {"form": form}
    return render(request, "blog/post_form.html", context)


@user_passes_test(lambda user: user.is_autor, login_url="posts")
@login_required(login_url="login")
def update_post(request, pk):
    profile = request.user.profile
    post = profile.user.autor.post_set.get(id=pk)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect("posts")

    context = {"form": form}
    return render(request, "blog/post_form.html", context)


@user_passes_test(lambda user: user.is_autor, login_url="posts")
@login_required(login_url="login")
def delete_post(request, pk):
    profile = request.user.profile
    post = profile.user.autor.post_set.get(id=pk)
    if request.method == "POST":
        post.delete()
        return redirect("posts")

    context = {"object": post}
    return render(request, "delete_template.html", context)
