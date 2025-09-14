from django.shortcuts import render


# Create your views here.


# view for apiview
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json
import random
from django.http import JsonResponse
import os
from . import serializers



class RandomRecipe(APIView):
    """Test API View
    with this we can add get, post, patch, delete methods"""

    # def get(self, request, format=None):
    #     """Returns alist of APIViews"""
    #     an_apiview = [
    #         "Hi There!",
    #         "this the test api",
    #         "If you are seeing this ouput then you have successfully connected with this api"
    #     ]
    #     return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def get(self, request):
            json_path = os.path.join(os.path.dirname(__file__), 'recipes.json')

            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            recipe_keys  = list(data['recipes'].keys())

            random_recipe_key = random.choice(recipe_keys)

            random_recipe = data['recipes'][random_recipe_key]

            response_data = {
                "recipe_name": random_recipe_key,
                "ingredients": random_recipe['ingredients'],
                "instructions": random_recipe['method'],
                "tips": random_recipe['tips']
            }

            return JsonResponse(response_data)


from rest_framework import viewsets

from RecipeDB import models

from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from RecipeDB import permissions



class RecipeViewset(viewsets.ViewSet):
    """Test API Viewset"""
    serializer_class = serializers.RecipeSerializer



    def list(self, request):
        """Return a message"""
        recipe_viewset = [
            "Uses actions (list, create, retrieve, update, partial_update)",
            "Automatically maps to URLS using Routers",
            "Provides more functionality with less code"
        ]

        return Response({'message': 'Hello!', 'recipe_viewset': recipe_viewset})

        def search(self, request):
            """Return a message"""
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                name = serializer.validated_data.get('name')

                json_path = os.path.join(os.path.dirname(__file__), 'recipes.json')

                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if name in data['recipes']:
                    recipe = data['recipes'][name]
                    response_data = {
                        "recipe_name": name,
                        "ingredients": recipe['ingredients'],
                        "instructions": recipe['method'],
                        "tips": recipe['tips']
                    }
                    return JsonResponse(response_data)
                else:
                    return Response({'error': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)


            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

        def retrieve(self, request, pk=None):
            """Handle getting an object by its ID"""
            return Response({'http_method': 'GET'}) 

        def update(self, request, pk=None):
            """Handle updating an object"""
            return Response({'http_method': 'PUT'})

        def partial_update(self, request, pk=None):
            """Handle updating part of an object"""
            return Response({'http_method': 'PATCH'})

        def destroy(self, request, pk=None):
            """Handle removing an object""" 
            return Response({'http_method': 'DELETE'})





class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)