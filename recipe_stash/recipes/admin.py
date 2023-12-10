from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Comment, Tag, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'bio', 'public')


class IngredientAdmin(admin.ModelAdmin):
    display = ('name')


class IngredientInRecipe(admin.TabularInline):
    model = RecipeIngredient


class CommentsInRecipe(admin.TabularInline):
    model = Comment


class RecipeAdmin(admin.ModelAdmin):
    display = ('title', 'author', 'date')
    inlines = [IngredientInRecipe, CommentsInRecipe]


class TagAdmin(admin.ModelAdmin):
    list_display = ('name')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
