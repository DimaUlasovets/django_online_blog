from django.urls import path
from users import views

urlpatterns = [
    path("", views.profiles, name="profiles"),
    path("profile/<str:pk>/", views.user_profile, name="user_profile"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("signup/autor/", views.autor_signup, name="autor_signup"),
    path("signup/reader/", views.reader_signup, name="reader_signup"),
    path("account/", views.user_account, name="account"),
    path("edit_account/", views.edit_account, name="edit_account"),
    path("create_categories/", views.create_categories, name="create_categories"),
    path("update_categories/<str:pk>/", views.update_categories, name="update_categories"),
    path("delete_categories/<str:pk>/", views.delete_categories, name="delete_categories"),
]
