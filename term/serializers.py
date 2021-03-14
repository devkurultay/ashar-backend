from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('slug', 'title')


class OtherLanguageExampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = OtherLangExample
        fields = ('translation', 'language',)

    def validate(self, attrs):
        if attrs.get('translation') is None:
            raise serializers.ValidationError("translation field required")
        elif attrs.get('language') is None:
            raise serializers.ValidationError("language field required")
        return attrs


class OtherLanguageExampleRepresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = OtherLangExample
        fields = ('translation', 'language')


class SuggestionRepresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Suggestion
        fields = ('author', 'suggested_translation')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        return representation


class TermSerializer(serializers.ModelSerializer):
    other_lang_examples = OtherLanguageExampleSerializer(many=True, write_only=True)
    category = serializers.SlugField()

    class Meta:
        model = Term
        fields = ('id', 'other_lang_examples', 'term', 'description', 'category')

    def validate(self, attrs):
        category_slug = attrs.get('category')
        if not Category.objects.filter(slug=category_slug).exists():
            raise serializers.ValidationError("category not found")
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        category_slug = validated_data.pop('category')
        category = Category.objects.get(slug=category_slug)
        other_lang_examples = validated_data.pop('other_lang_examples')
        term = Term.objects.create(author=request.user, category=category, **validated_data)
        for other_lang in other_lang_examples:
            OtherLangExample.objects.create(
                term=term,
                translation=other_lang['translation'],
                language=other_lang['language'],
            )
        return term

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['other_language_examples'] = OtherLanguageExampleRepresentationSerializer(
            instance.other_lang_examples.all(), many=True, context=self.context).data
        representation['translation_suggestions'] = SuggestionRepresentationSerializer(
            instance.suggestions.only('author', 'suggested_translation'), many=True, context=self.context).data
        return representation


class TermUpdateDeleteSerializer(serializers.ModelSerializer):
    other_lang_examples = OtherLanguageExampleSerializer(many=True, read_only=True)

    class Meta:
        model = Term
        fields = ('id', 'other_lang_examples', 'term', 'description', 'category')

    def validate(self, attrs):
        category_slug = attrs.get('category').slug
        if not Category.objects.filter(slug=category_slug).exists():
            raise serializers.ValidationError("category not found")
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        category_slug = validated_data.pop('category')
        category = Category.objects.get(slug=category_slug)
        other_lang_examples = validated_data.pop('other_lang_examples')
        term = Term.objects.create(author=request.user, category=category, **validated_data)
        for other_lang in other_lang_examples:
            OtherLangExample.objects.create(
                term=term,
                translation=other_lang['translation'],
                language=other_lang['language'],
            )
        return term

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['other_language_examples'] = OtherLanguageExampleRepresentationSerializer(
            instance.other_lang_examples.all(), many=True, context=self.context).data
        representation['translation_suggestions'] = SuggestionRepresentationSerializer(
            instance.suggestions.only('author', 'suggested_translation'), many=True, context=self.context).data
        return representation


class SuggestionSerializer(serializers.ModelSerializer):
    term_id = serializers.IntegerField(required=True)

    class Meta:
        model = Suggestion
        fields = ('suggested_translation', 'term_id',)

    def create(self, validated_data):
        term_id = validated_data.pop('term_id')
        term = Term.objects.filter(id=term_id).first()
        request = self.context.get('request')
        suggestion = Suggestion.objects.create(
            author=request.user, term=term, **validated_data
        )
        return suggestion
