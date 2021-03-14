from rest_framework import generics, permissions

from like.models import Like
from like.serializers import LikeSerializer


class LikeListCreateView(generics.ListCreateAPIView):
    queryset = Like.objects.select_related('author')
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_serializer_context(self):
        return {'request': self.request}
