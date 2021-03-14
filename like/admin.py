from django.contrib import admin

from like.models import Like, SuggestionLike

admin.site.register(Like)
admin.site.register(SuggestionLike)
