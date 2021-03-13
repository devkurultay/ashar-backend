from django.urls import path

from term import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view()),
    path('terms/', views.TermListCreateView.as_view()),
    path('term-detail/<int:pk>/', views.TermDetailView.as_view()),
    path('term/<int:pk>/', views.TermUpdateDeleteView.as_view()),
    path('suggestion/', views.SuggestionView.as_view()),
]
