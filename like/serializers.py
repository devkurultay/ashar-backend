from django.contrib.auth import get_user_model
from rest_framework import serializers

from like.models import Like, SuggestionLike
from term.models import Suggestion

User = get_user_model()


class LikeSerializer(serializers.ModelSerializer):
    suggestion_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Like
        fields = ('id', 'like', 'suggestion_id')

    def validate(self, attrs):
        request = self.context.get('request')
        if not attrs['like'] == 1:
            raise serializers.ValidationError("you cannot set other number, except 1")
        if Like.objects.filter(
                author=request.user, suggestionslikes__suggestion_id__in=[attrs['suggestion_id']]).exists():
            raise serializers.ValidationError("you cannot like more than one time")
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        suggestion_id = validated_data.pop('suggestion_id')
        suggestion = Suggestion.objects.filter(id=suggestion_id).first()
        like = Like.objects.create(author=request.user, **validated_data)
        SuggestionLike.objects.create(
            like=like,
            suggestion=suggestion
        )
        return suggestion

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['suggestion'] = instance.suggestionslikes.first().suggestion.suggested_translation
        representation['like'] = instance.suggestionslikes.count()
        return representation
