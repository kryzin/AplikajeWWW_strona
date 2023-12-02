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


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ['recipe', 'ingredient', 'quantity', 'unit_of_measurement']

    # def create(self, validated_data):
    #     ingredient_data = validated_data.pop('ingredient')
    #     ingredient = Ingredient.objects.create(**ingredient_data)
    #     recipe_ingredient = RecipeIngredient.objects.create(ingredient=ingredient, **validated_data)
    #     return recipe_ingredient


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
    recipe_ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        read_only_fields = ['id']
        fields = '__all__'

    # def create(self, validated_data):
    #     # this is so that you can create the ingredients while creating a recipe
    #     # when writing a json request you would do:
    #     # {"recipe":"Recipe1","ingredient":"{"name":"Flour"}, "quantity":"300", "unit_of_mesure":"grams"}
    #     # the inner {} define a Ingredient Objects, the outer {} define a RecipeIngredient Object
    #
    #     recipe_ingredients_data = validated_data.pop('recipe_ingredients')
    #     recipe = Recipe.objects.create(**validated_data)
    #     for recipe_ingredient_data in recipe_ingredients_data:
    #         # Recipe creates RecipeIngredient and RecipeIngredient creates Ingredient
    #         RecipeIngredient.objects.create(recipe=recipe, **recipe_ingredient_data)
    #     return recipe