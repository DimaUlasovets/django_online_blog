import uuid

from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from django.dispatch import receiver


class User(AbstractUser):

    is_autor = models.BooleanField(default=False)
    is_reader = models.BooleanField(default=False)


class Reader(models.Model):
    class Meta:
        verbose_name = "Reader"
        verbose_name_plural = "Readers"

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user.is_reader = True

    def __str__(self):
        return self.user.get_username()


class Autor(models.Model):
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autors"

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user.is_autor = True
    company = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.get_username()


class Profile(models.Model):
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=500, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="profiles/", default="profiles/user-default.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_username()


class Categories(models.Model):
    class Meta:
        verbose_name = "Categori"
        verbose_name_plural = "Categories"

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    autor_id = models.ForeignKey(Autor, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
