from rest_framework import generics, permissions

from .models import Category, Term, Suggestion
from .serializers import (
    CategorySerializer, TermSerializer, SuggestionSerializer
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.only('title', 'slug')
    serializer_class = CategorySerializer


class TermListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Term.objects.select_related('author', 'category')
    serializer_class = TermSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class TermDetailView(generics.RetrieveAPIView):
    queryset = Term.objects.select_related('author', 'category')
    serializer_class = TermSerializer


class TermUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Term.objects.select_related('author', 'category')
    serializer_class = TermSerializer


class SuggestionView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Suggestion.objects.select_related('author', 'term')
    serializer_class = SuggestionSerializer
