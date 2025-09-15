from rest_framework import serializers

# from .models import UserProfile

from .models import Recipe
from django.contrib.auth.models import User

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'method', 'tips'] 
        # read_only_fields = ['__all__'] # By Default django manages it to read-only




# class UserSerializer(serializers.ModelSerializer):
#     Recipe = RecipeSerializer(many=True, read_only=True)

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'Recipe']
#         read_only_fields = ['__all__']










# class RecipeSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     ingredients = serializers.ListField(child=serializers.CharField())
#     method = serializers.ListField(child=serializers.CharField())
#     tips = serializers.ListField(child=serializers.CharField())


# class UserProfileSerializer(serializers.ModelSerializer):
#     """Serializes a user profile object"""

#     class Meta:
#         model = UserProfile
#         fields = ('id', 'email', 'name', 'password')
#         extra_kwargs = {
#             'password': {
#                 'write_only': True,
#                 'style': {'input_type': 'password'}
#             }
#         }

#     def create(self, validated_data):
#         """Create and return a new user"""
#         user = UserProfile.objects.create_user(
#             email=validated_data['email'],
#             name=validated_data['name'],
#             password=validated_data['password']
#         )

#         return user

#     def update(self, instance, validated_data):
#         """Handle updating user account"""
#         if 'password' in validated_data:
#             password = validated_data.pop('password')
#             instance.set_password(password)

#         return super().update(instance, validated_data)




