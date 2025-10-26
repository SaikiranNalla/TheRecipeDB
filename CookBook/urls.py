from django.urls import path
from . import views

app_name = 'CookBook'

urlpatterns = [
   # Main pages
    path('', views.home, name='home'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('selected/', views.selected_recipes_view, name='selected_recipes'),
    path('grocery-list/', views.grocery_list_view, name='grocery_list'),
    path('about/', views.about, name='about'),
    path('api-docs/', views.api_docs, name='api_docs'),


    # AJAX endpoints for recipe selection
    path('select/<int:recipe_id>/', views.select_recipe, name='select_recipe'),
    path('deselect/<int:recipe_id>/', views.deselect_recipe, name='deselect_recipe'),
    path('generate-grocery-list/', views.generate_grocery_list, name='generate_grocery_list'),
    
    # Clear selection
    path('clear-selection/', views.clear_selection, name='clear_selection'),
]