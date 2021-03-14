from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView

from comment.models import Comment
from comment.serializers import CommentCreateSerializer, CommentSerializer


class CommentCreateView(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Comment.objects.select_related('author', 'suggestion')
    serializer_class = CommentCreateSerializer


class CommentListView(ListAPIView):
    queryset = Comment.objects.select_related('author', 'suggestion')
    serializer_class = CommentSerializer


