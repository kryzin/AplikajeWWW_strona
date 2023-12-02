from datetime import date

from rest_framework import serializers
from .models import Profile, Ingredient, RecipeIngredient, Recipe, RecipeTag, Comment, Tag
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        read_only_fields = ['id', 'creation_date', 'owner']
        fields = ['id', 'name', 'username', 'bio', 'public', 'creation_date', 'owner']

    def validate_name(self, value): # only letters + space
        if not all(char.isalpha() or char == ' ' for char in value):
            raise serializers.ValidationError(f"{date.today()} Nazwa może zawierać tylko litery.")
        return value

    def update(self, instance, validated_data): # override for validation
        instance.name = validated_data.get('name', instance.name)
        self.validate_name(instance.name)
        instance.save()
        return instance


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        read_only_fields = ['id']
        fields = '__all__'