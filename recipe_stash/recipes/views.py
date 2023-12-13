from django.http import HttpResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from .models import Profile, Recipe
from .serializers import RecipeSerializer, CommentSerializer, ProfileCreationSerializer, ProfileSerializer, ProfileListSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework import permissions
import copy
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.decorators import login_required
from .forms import CreationForm


def index(request):
    return HttpResponse("This is a Recipe Management Website.")

@api_view(['POST'])
def profile_create(request):
    """
    create a new Profile (AbstractUser)
    input: username, password, email, public(bool)
    """
    serializer = ProfileCreationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def profile_detail(request, pk):
    """
    Show Profile(id=pk)
    For everyone, shows only if public (admin overrides)
    """
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if profile.public or request.user.is_staff: # show only if public/ is admin
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

@login_required # just to redirect to login if not logged-in
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def myprofile_detail(request):
    """
    See/Edit/Delete your own Profile
    """
    profile = request.user
    serializer = ProfileSerializer(profile)
    if request.method == 'GET':
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def profile_list(request):
    """
    All Public Profiles,
    AdminOnly: All Profiles
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_staff:
                profiles = Profile.objects.all() # all for admin - staff
            else:
                profiles = Profile.objects.filter(public=True) # only public profiles
        serializer = ProfileListSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def recipe_list(request):
    """
    Show all recipes of public profiles,
    ignore public=false for admin
    """
    if request.method == 'GET':
        recipes = Recipe.objects.filter(author__public=True)
        if request.user.is_staff:
            recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def recipe_detail(request, pk):
    """
    Show Recipe(id=pk) (only if public=true or user=author)
    Edit/Delete Recipe if request.user = author
    """
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if recipe.author.public or request.user.is_staff: # show only if public/ is admin
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'PUT' or request.method == 'DELETE':
        if request.user == recipe.author:
            if request.method == 'PUT':
                serializer = RecipeSerializer(recipe)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if request.method == 'DELETE':
                recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def recipes_by_author(request, pk):
    """
    Show all recipes of author=Profile(id=pk),
    *obv only if public profile
    """
    if request.method == 'GET':
        author = Profile.objects.get(pk=pk)
        if author.public:
            recipes = Recipe.objects.filter(author__pk=pk)
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def recipes_by_tag(request, substr):
    """
    Show all recipes with (tags contains Tag(name=substr))
    """
    if request.method == 'GET':
        recipes = Recipe.objects.filter(tags__name__icontains=substr, author__public=True)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([])
def recipes_by_title(request, substr):
    """
    Show recipes with title containing substr
    """
    if request.method == 'GET':
        recipes = Recipe.objects.filter(title__icontains=substr, author__public=True)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def recipes_with_ingredients(request):
    """
    input ingredients as list in url: /?ingredients=milk,flour,fish
    """
    ingredients = request.query_params.get('ingredients', '').split(',')
    recipes = Recipe.objects.filter(author__public=True)
    for ing in ingredients:
        recipes = recipes.filter(ingredients__ingredient__name__icontains=ing)
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST', 'DELETE'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def comment_create(request, pk):
    """
    post a new comment - by you
    """
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
