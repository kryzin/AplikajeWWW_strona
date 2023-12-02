from django.db import models
from markdownx.models import MarkdownxField
from django.contrib.auth.models import User
from datetime import date


class Profile(models.Model):  # later just connect as User adjacent
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    bio = models.TextField()
    public = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.username} ({self.name})"


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
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    preparation_time = models.DurationField()
    overall_time = models.DurationField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    instructions = MarkdownxField(null=True)
    tags = models.ManyToManyField(Tag, through='RecipeTag')
    # rating = models.FloatField()

    def __str__(self):
        return f"{self.title} - {self.author}"


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit_of_measurement = models.CharField(max_length=20)  # add choices for units


class Comment(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.recipe.title} - {self.content}"


# users can add recipes to favs, develop into different kinds? different titles for collections of recipes
# class Favourites(models.Model):
#     recipe =
#     user =