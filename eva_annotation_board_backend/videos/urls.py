from django.urls import path
from . import views


urlpatterns = [
    path("", views.VideosView.as_view()),
    path("search", views.VideoSearchView.as_view()),
    path("<int:pk>", views.VideoView.as_view()),
]
