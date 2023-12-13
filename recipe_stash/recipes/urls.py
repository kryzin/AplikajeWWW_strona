from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/', views.profile_list),
    path('new-profile/', views.profile_create),
    path('profile/<int:pk>/', views.profile_detail),
    path('myprofile/', views.myprofile_detail),

    path('recipes/', views.recipe_list),
    path('recipe/<int:pk>/', views.recipe_detail),
    path('recipes-by-author/<int:pk>/', views.recipes_by_author),
    path('recipes-by-tag/<str:substr>', views.recipes_by_tag),
    path('recipes-by-title/<str:substr>', views.recipes_by_title),
    path('recipes-with-ingredients/', views.recipes_with_ingredients),

    path('comment/<int:pk>', views.comment_create),
]
