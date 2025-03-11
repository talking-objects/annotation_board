from django.urls import path
from . import views

urlpatterns = [
    path("", views.EditVideoViews.as_view()),
    path("<int:pk>", views.EditVideoDetailViews.as_view()),
]
