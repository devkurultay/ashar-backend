from django.db.models import Q
from rest_framework import generics, permissions

from .models import Category, Term, Suggestion
from .serializers import (
    CategorySerializer, TermSerializer, SuggestionSerializer, TermUpdateDeleteSerializer
)
from .permissions import IsAuthorPermission


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.only('title', 'slug')
    serializer_class = CategorySerializer


class TermListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Term.objects.select_related('author', 'category')
    serializer_class = TermSerializer

    def get_queryset(self):
        queryset = Term.objects.select_related('author', 'category')
        filter = self.request.query_params.get('filter')
        search = self.request.query_params.get('search')
        if filter:
            queryset = Term.objects.filter(category__slug=filter)
        elif search:
            queryset = Term.objects.filter(Q(term__icontains=search) | Q(description__icontains=search))
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}


class TermDetailView(generics.RetrieveAPIView):
    queryset = Term.objects.select_related('author', 'category')
    serializer_class = TermSerializer


class TermUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Term.objects.select_related('author', 'category')
    serializer_class = TermUpdateDeleteSerializer
    permission_classes = (IsAuthorPermission, )


class SuggestionView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Suggestion.objects.select_related('author', 'term')
    serializer_class = SuggestionSerializer
