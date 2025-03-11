from django.urls import path
from . import views

urlpatterns = [
    path("", views.ClipView.as_view()),
    path("search", views.ClipSearchView.as_view()),
    path("<int:pk>", views.ClipDetailView.as_view()),
]
