from blog.models import Post, Tag
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from users.forms import CategoriesForm, ProfileForm, RegisterForm
from users.models import Autor, Profile, Reader, User

# Create your views here.


def login_user(request):

    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, "users/login.html")


def logout_user(request):
    logout(request)
    messages.info(request, "User was logged out")
    return redirect("login")


def signup_view(request):
    return render(request, "users/signup.html")


def autor_signup(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.username = user.username.lower()
            user.is_autor = True
            user.save()

            Autor.objects.create(user=user)
            messages.success(request, "Autor account was created")

            login(request, user)
            return redirect("edit_account")

        else:
            messages.success(request, "An error has occured during registration")
            form = RegisterForm()

    context = {"form": form}

    return render(request, "users/autor_signup.html", context)


def reader_signup(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.username = user.username.lower()
            user.is_reader = True
            user.save()

            Reader.objects.create(user=user)
            messages.success(request, "Reader account was created")

            login(request, user)
            return redirect("edit_account")

        else:
            messages.success(request, "An error has occured during registration")
            form = RegisterForm()

    context = {"form": form}

    return render(request, "users/reader_signup.html", context)


def profiles(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    profiles = Profile.objects.filter(user__is_autor=True, name__icontains=search_query)
    context = {"profiles": profiles, "search_query": search_query}
    return render(request, "users/profiles.html", context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    categories = profile.user.autor.categories_set.all()

    context = {
        "profile": profile,
        "categories": categories,
    }
    return render(request, "users/user_profile.html", context)


@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile

    if request.user.is_autor:
        categories = profile.user.autor.categories_set.all()
        context = {
            "profile": profile,
            "categories": categories,
        }
    else:
        context = {"profile": profile}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("account")

    context = {"form": form}

    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def create_categories(request):
    form = CategoriesForm()
    profile = request.user.profile

    if request.method == "POST":
        form = CategoriesForm(request.POST)
        if form.is_valid():
            categori = form.save(commit=False)
            categori.autor_id = profile.user.autor
            categori.save()

            return redirect("account")

    context = {"form": form}
    return render(request, "users/categori_form.html", context)


@login_required(login_url="login")
def update_categories(request, pk):
    profile = request.user.profile
    categori = profile.user.autor.categories_set.get(id=pk)
    form = CategoriesForm(instance=categori)

    if request.method == "POST":
        form = CategoriesForm(request.POST, instance=categori)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated")

            return redirect("account")

    context = {"form": form}
    return render(request, "users/categori_form.html", context)


@login_required(login_url="login")
def delete_categories(request, pk):
    profile = request.user.profile
    categori = profile.user.autor.categories_set.get(id=pk)

    if request.method == "POST":
        categori.delete()
        messages.success(request, "Skill was deleted")

        return redirect("account")

    context = {"object": categori}
    return render(request, "delete_template.html", context)
