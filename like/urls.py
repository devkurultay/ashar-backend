from django.urls import path
from . import views

urlpatterns = [
    path('like/', views.LikeListCreateView.as_view())
]
