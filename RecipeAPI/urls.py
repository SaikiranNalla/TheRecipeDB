from django.urls import path, include
from RecipeAPI import views

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('recipe', views.RecipeViewset, basename='recipe')
# router.register('profile', views.UserProfileViewSet)


urlpatterns = [
    # path('random/', views.RandomRecipe.as_view(), name='RecipeView'),
    # path('', include(router.urls)),
    path('random/', views.random_recipe, name='random_recipe'),
    
]












# @api_view decorator, the URL pattern should directly point to that function without using .as_view(). This is the simplest and most direct approach for your single-endpoint API.

# urls.py
# from django.urls import path

# from . import views # Assuming views.py is in the same app directory

# urlpatterns = [
#     path('random/', views.random_recipe, name='random-recipe'),
# ]

# This corrected urls.py will work perfectly with your random_recipe function.
# ​Correct urls.py for a ViewSet (For Context)




# ​If you wanted to use the ViewSet approach for a full CRUD API, the urls.py would look like this:

# urls.py
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# router = DefaultRouter()
# router.register('recipes', views.RecipeViewSet, basename='recipe')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

# ​This single include(router.urls) line would automatically generate multiple URL patterns for you, such as /recipes/, /recipes/<pk>/, etc.
# ​Final Recommendation
# ​Based on your goal of creating a single API endpoint to retrieve a random recipe, stick with the @api_view approach. The corrected urls.py for this approach is the most efficient and clear solution. Remove the router configuration and the extra imports to keep your code clean and focused on your objective.

