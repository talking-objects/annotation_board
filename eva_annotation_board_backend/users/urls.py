from django.urls import path
from . import views

urlpatterns = [
    path("me", views.MeView.as_view()),
    path("", views.UserView.as_view()),
    path("log-in", views.LogInView.as_view()),
    path("log-out", views.LogOutView.as_view()),
]
