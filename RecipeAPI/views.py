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


# from rest_framework import viewsets

# from RecipeAPI import models

# from rest_framework.authentication import TokenAuthentication
# from rest_framework import filters
# from RecipeAPI import permissions






# class RecipeViewset(viewsets.ViewSet):
#     """Test API Viewset"""
#     serializer_class = serializers.RecipeSerializer



#     def list(self, request):
#         """Return a message"""
#         recipe_viewset = [
#             "Uses actions (list, create, retrieve, update, partial_update)",
#             "Automatically maps to URLS using Routers",
#             "Provides more functionality with less code"
#         ]

#         return Response({'message': 'Hello!', 'recipe_viewset': recipe_viewset})

#         def search(self, request):
#             """Return a message"""
#             serializer = self.serializer_class(data=request.data)

#             if serializer.is_valid():
#                 name = serializer.validated_data.get('name')

#                 json_path = os.path.join(os.path.dirname(__file__), 'recipes.json')

#                 with open(json_path, 'r', encoding='utf-8') as f:
#                     data = json.load(f)
                
#                 if name in data['recipes']:
#                     recipe = data['recipes'][name]
#                     response_data = {
#                         "recipe_name": name,
#                         "ingredients": recipe['ingredients'],
#                         "instructions": recipe['method'],
#                         "tips": recipe['tips']
#                     }
#                     return JsonResponse(response_data)
#                 else:
#                     return Response({'error': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)


#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

#         def retrieve(self, request, pk=None):
#             """Handle getting an object by its ID"""
#             return Response({'http_method': 'GET'}) 

#         def update(self, request, pk=None):
#             """Handle updating an object"""
#             return Response({'http_method': 'PUT'})

#         def partial_update(self, request, pk=None):
#             """Handle updating part of an object"""
#             return Response({'http_method': 'PATCH'})

#         def destroy(self, request, pk=None):
#             """Handle removing an object""" 
#             return Response({'http_method': 'DELETE'})





# class UserProfileViewSet(viewsets.ModelViewSet):
#     """Handle creating and updating profiles"""
#     serializer_class = serializers.UserProfileSerializer
#     queryset = models.UserProfile.objects.all()

#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (permissions.UpdateOwnProfile,)
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('name', 'email',)


from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# class RecipeViewset(viewsets.ModelViewSet):
#     """Handle creating, creating and updating profiles"""
#     queryset = models.Recipe.objects.all()
#     serializer_class = serializers.RecipeSerializer

#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         """Sets the user profile to the logged in user"""
#         serializer.save(user=self.request.user)

#     def get_queryset(self):
#         return Recipe.objects.filter(user=self.request.user)


# Alternative view using order_by('?')

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Recipe
from .serializers import RecipeSerializer

@api_view(['GET'])
def random_recipe(request):
    recipe = Recipe.objects.order_by('?').first()
    if not recipe:
        return Response({"detail": "No recipes found."}, status=404)
    
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data)




























# ​@api_view
# ​The @api_view decorator is the simplest way to create a DRF view. It's used with function-based views.
# ​What it is: A decorator that wraps a regular Django function, making it an API view that can handle specific HTTP methods like GET, POST, PUT, etc.
# ​Use case: Ideal for simple, single-endpoint views that don't fit into a standard CRUD (Create, Retrieve, Update, Delete) pattern, such as the random recipe API you're building.
# ​How it works: You pass a list of allowed HTTP methods to the decorator (e.g., @api_view(['GET'])). The function itself contains the logic for that specific request.
# ​APIView
# ​APIView is the class-based equivalent of a function-based view. It's a fundamental building block in DRF for creating more complex views.
# ​What it is: A class that inherits from DRF's APIView base class. You define methods like get(), post(), put(), and delete() to handle the corresponding HTTP requests.
# ​Use case: Best for views that require more structured logic, such as using permissions, authentication, or renderers. It provides a more organized way to handle multiple HTTP methods in a single view.
# ​How it works: You create a class that inherits from APIView and override the appropriate methods. For example, the get() method would contain the logic for a GET request.
# ​ViewSets
# ​ViewSets are a higher-level abstraction that group a set of related views into a single class. They are specifically designed for building API endpoints that correspond to a single model.
# ​What it is: A class that inherits from a ViewSet base class (like ModelViewSet). It provides actions like list, retrieve, create, update, and destroy for a resource.
# building full-fledged APIs.​Use case: Perfect for building RESTful APIs where you have a set of standard operations (CRUD) on a single model. They simplify URL routing and reduce code repetition.
# ​How it works: You create a class that inherits from ModelViewSet, define the queryset and serializer_class, and DRF automatically generates the list, retrieve, create, etc., methods for you. You then register the ViewSet with a router to automatically generate the URL patterns. This makes it extremely efficient for 




