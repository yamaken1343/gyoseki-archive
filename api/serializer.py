from rest_framework import serializers
from gyoseki.models import Recode, Author, Language, Division, Tag


class RegisterSerializer(serializers.ModelSerializer):
    main_author = serializers.SlugRelatedField(queryset= Author.objects.all(), slug_field='name')
    language = serializers.SlugRelatedField(slug_field='name', queryset= Language.objects.all())
    division = serializers.SlugRelatedField(slug_field='name', queryset= Division.objects.all())
    tag = serializers.SlugRelatedField(slug_field='name', queryset= Tag.objects.all(), many=True)

    class Meta:
        model = Recode
        exclude = []
