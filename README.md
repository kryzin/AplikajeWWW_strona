
# RecipeStash - recipe-sharing forum

## Database

![](img/db.sqlite3%20-%20recipes_recipe.png)
- Main models: Recipe, User(author in recipe), Ingredient, Tag, Comment
*not yet: Favourites or Collections to group 'saved' recipes*
- Models aiding in relations: RecipeIngredient, RecipeTag

## Endpoints (wip)

- CRUD Recipe, User, Ingredient, Tag, Comment
- Search for recipe by tag, by ingredients, by author
- Adding recipes to and creating Favourites lists
- Get most viewed/commented recipe on front page