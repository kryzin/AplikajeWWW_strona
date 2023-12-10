from django.db import models
from markdownx.models import MarkdownxField
from django.contrib.auth.models import AbstractUser
from datetime import date


class Profile(AbstractUser):  # overrides django default auth user
    bio = models.TextField()
    public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.username})"


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    preparation_time = models.DurationField()
    overall_time = models.DurationField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    instructions = MarkdownxField(null=True)
    tags = models.ManyToManyField(Tag)
    # rating = models.FloatField()

    def __str__(self):
        return f"{self.title} - {self.author}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)


class Comment(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.recipe.title} - {self.content}"
