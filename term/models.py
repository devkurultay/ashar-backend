from django.contrib.auth import get_user_model
from pytils.translit import slugify
from django.db import models


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Имя категории')
    slug = models.SlugField(primary_key=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Term(models.Model):
    term = models.CharField(max_length=200)
    description = models.TextField()
    active = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='terms')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_terms')

    def __str__(self):
        return self.term


class OtherLangExample(models.Model):
    LANG_RU = 'ru'
    LANG_EN = 'en'
    LANG_TR = 'tr'

    CHOICES_LANGUAGE = (
        (LANG_RU, 'Russian'),
        (LANG_EN, 'English'),
        (LANG_TR, 'Turkish'),
    )

    translation = models.CharField(max_length=150, blank=True, verbose_name='Перевод')
    language = models.CharField(max_length=150, choices=CHOICES_LANGUAGE, verbose_name='Выбор языка', blank=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='other_lang_examples')

    def __str__(self):
        return self.translation


class Suggestion(models.Model):
    suggested_translation = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggestions')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='suggestions')

    def __str__(self):
        return self.suggested_translation
