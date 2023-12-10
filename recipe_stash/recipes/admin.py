from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Comment, Tag, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'bio', 'public')


class IngredientAdmin(admin.ModelAdmin):
    display = ('name')


class IngredientInRecipe(admin.TabularInline):
    model = RecipeIngredient


class TagsInRecipe(admin.TabularInline):
    model = Recipe.tags.through


class CommentsInRecipe(admin.TabularInline):
    model = Comment


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    inlines = [IngredientInRecipe, TagsInRecipe, CommentsInRecipe]


class TagAdmin(admin.ModelAdmin):
    list_display = ('name')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
