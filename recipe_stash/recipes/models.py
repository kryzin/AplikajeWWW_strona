from django.db import models
from markdownx.models import MarkdownxField


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    TYPE_CHOICES = [
        ('breakfast', 'breakfast'),
        ('lunch', 'lunch'),
        ('dinner', 'dinner'),
        ('dessert', 'dessert'),
        ('snack', 'snack'),
        ('other', 'other'),
    ]

    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    preparation_time = models.DurationField()
    overall_time = models.DurationField()
    recipe_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    instructions = MarkdownxField(null=True)
    # rating = models.FloatField()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit_of_measurement = models.CharField(max_length=20)  # add choices for units


class Author(models.Model):  # later replace with AbstractUser or other auth alt
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    bio = models.TextField()
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.name
