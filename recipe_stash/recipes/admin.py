from django.contrib import admin

from .models import User, Ingredient, Recipe, RecipeIngredient, Comment, Tag, RecipeTag

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'public')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)


class IngredientInRecipe(admin.TabularInline):
    model = RecipeIngredient


class TagsInRecipe(admin.TabularInline):
    model = RecipeTag


class CommentsInRecipe(admin.TabularInline):
    model = Comment


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    inlines = [IngredientInRecipe, TagsInRecipe, CommentsInRecipe]


class TagAdmin(admin.ModelAdmin):
    list_display = ('name')

admin.site.register(User, UserAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
