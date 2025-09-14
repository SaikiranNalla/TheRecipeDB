from django.urls import path, include
from RecipeDB import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recipe', views.RecipeViewset, basename='recipe')
router.register('profile', views.UserProfileViewSet)


urlpatterns = [
    path('random/', views.RandomRecipe.as_view(), name='RecipeView'),
    path('', include(router.urls))

]