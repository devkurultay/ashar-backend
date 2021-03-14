from django.contrib.auth import get_user_model
from django.db import models

from term.models import Suggestion

User = get_user_model()


class Like(models.Model):
    like = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.author.email} - {self.like}"


class SuggestionLike(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE, related_name='suggestionslikes')
    like = models.ForeignKey(Like, on_delete=models.CASCADE, related_name='suggestionslikes')

    def __str__(self):
        return f"{self.like.author}"

    @property
    def get_like_count(self):
        return self.suggestion.suggestionslikes.count()
