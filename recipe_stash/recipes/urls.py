from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/', views.profile_list),
    path('new-profile/', views.profile_create),
    path('profile/<int:pk>/', views.profile_detail),
    path('myprofile/', views.myprofile_detail),

    path('recipes/', views.recipe_list),
]
