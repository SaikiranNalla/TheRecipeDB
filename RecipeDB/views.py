from django.shortcuts import render

# Create your views here.


# view for apiview
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RecipeView(APIView):
    """Test API View"""

    def get(self, request, format=None):
        """Returns alist of APIViews"""
        an_apiview = [
            "Hi There!",
            "this the test api",
            "If you are seeing this ouput then you have successfully connected with this api"
        ]
        return Response({'message': 'Hello!', 'an_apiview': an_apiview})