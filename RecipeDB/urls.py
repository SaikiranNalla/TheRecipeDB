from django.urls import path
from RecipeDB import views

urlpatterns = [
    path('hello/', views.RecipeView.as_view(), name='RecipeView')
]