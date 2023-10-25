from django.contrib import admin

from .models import Author, Ingredient, Recipe, RecipeIngredient

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'public')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)


class IngredientInRecipe(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'recipe_type')
    inlines = [IngredientInRecipe]

admin.site.register(Author, AuthorAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
