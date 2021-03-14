from django.urls import path

from . import views

urlpatterns = [
    path("comment/create/", views.CommentCreateView.as_view()),
]
