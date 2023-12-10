from django.http import HttpResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from .models import Profile, Recipe
from .serializers import RecipeSerializer, ProfileCreationSerializer, ProfileSerializer, ProfileListSerializer, TagSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework import permissions
import copy
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from .forms import CreationForm

# views still missing:
"""
TOKENSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS EVERYWHEREEEEE
CRUD for Ingredients etc.,
Comments: CRUD + see them in Recipe,
"""

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
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

@login_required
@api_view(['GET', 'PUT', 'DELETE'])
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

@login_required # LOGIN_URL set in settings
@api_view(['GET'])
def profile_list(request):
    """
    All Public Profiles
    AdminOnly: All Profiles
    """
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            if user.is_staff:
                profiles = Profile.objects.all() # all for admin - staff
            else:
                profiles = Profile.objects.filter(public=True) # only public profiles
        serializer = ProfileListSerializer(profiles, many=True)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def recipe_list(request):
    """
    Show all recipes of public profiles
    ignore public=false for admin
    """
    if request.method == 'GET':
        recipes = Recipe.objects.filter(author__public=True)
        if request.user.is_staff:
            recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def recipe_detail(request, pk):
    """
    Show Recipe(id=pk) (only if public=true or user=author)
    or also add edit if user=author
    """

@api_view([])
def recipes_by_author(request, pk):
    """
    can you also show profile all?
    Show all recipes of author=Profile(id=pk)
    """

@api_view([])
def recipes_by_tag(request, substr):
    """
    Show all recipes with (tags contains Tag(name=substr)) //or pk
    """

@api_view([])
def recipes_by_title(request, substr):
    """
    Show recipes with title containing substr
    """

@api_view([])
def recipes_with_ingredients(request):
    """
    input ingredients as list in url: /ingredients=milk&flour&fish
    """
# class RecipeDetail(APIView):
#     """
#     + add auth that only author can edit
#     CRUD
#     Get/Update/Create/Delete a Recipe object with given pk
#     """
#     def get_queryset(self):
#         return Recipe.objects.all()
#
#     def get_object(self, pk):
#         try:
#             return Recipe.objects.get(pk=pk)
#         except Recipe.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         recipe = self.get_object(pk)
#         serializer = RecipeSerializer(recipe)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         recipe = self.get_object(pk)
#         serializer = RecipeSerializer(recipe, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         print(serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def post(self, request, format=None):
#         serializer = RecipeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         recipe = self.get_object(pk)
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class RecipeList(APIView):
#     """
#     + everyone can see all recipes (of public accounts)
#     All Recipe Objects
#     """
#     def get(self, request, format=None):
#         recipes = Recipe.objects.all()
#         serializer = RecipeSerializer(recipes, many=True)
#         return Response(serializer.data)
#
#
# class TagDetail(APIView):
#     """
#     CRUD
#     Get/Update/Create/Delete a Tag object with given pk
#     """
#     def get_queryset(self):
#         return Tag.objects.all()
#
#     def get_object(self, pk):
#         try:
#             return Tag.objects.get(pk=pk)
#         except Tag.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         tag = self.get_object(pk)
#         serializer = TagSerializer(tag)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         tag = self.get_object(pk)
#         serializer = TagSerializer(tag, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         print(serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def post(self, request, format=None):
#         serializer = TagSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         tag = self.get_object(pk)
#         tag.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)