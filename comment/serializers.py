from rest_framework import serializers

from comment.models import Comment


class FilterCommentListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentCreateSerializer(serializers.ModelSerializer):
    """Добавление коммента"""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'parent', 'suggestion')


class CommentSerializer(serializers.ModelSerializer):
    """Вывод комментариев"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = ("id", "text", "children", "author", "suggestion")
