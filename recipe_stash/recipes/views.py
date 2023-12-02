# from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from .models import Profile, Recipe
from .serializers import RecipeSerializer, ProfileSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework import permissions
import copy

# views still missing:
"""
Create Recipe (with creating ingredients),
All Recipes,
CRUD Tag,
Comments: CRUD + see them in Recipe,
Register a new User -> Create a Profile,
Recipes of given Author, or Profile with all it's recipes,
Search for recipe by tags in url,
Search for recipe by ingredients in url
"""

def index(request):
    return HttpResponse("This is a Recipe Management Website.")


class ProfileDetail(APIView):
    """
    + add auth here for only the owner of the profile
    CRUD
    Get/Update/Delete a Profile object with given pk
    """
    def get_queryset(self):
        return Profile.objects.all()

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeDetail(APIView):
    """
    + add auth that only author can edit
    CRUD
    Get/Update/Create/Delete a Recipe object with given pk
    """
    def get_queryset(self):
        return Recipe.objects.all()

    def get_object(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        recipe = self.get_object(pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        recipe = self.get_object(pk)
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        recipe = self.get_object(pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)