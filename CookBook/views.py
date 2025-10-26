from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
import requests
import json

# Import Recipe model from RecipeAPI
from RecipeAPI.models import Recipe

# Import necessary for type and category filters
from django.db.models.functions import Lower, Trim, Coalesce



def home(request):
    """
    Homepage - Display all recipes with search and filter functionality
    """
    recipes = Recipe.objects.all().order_by('title')
    
    # Handle search query
    search_query = request.GET.get('search', '')
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(type__icontains=search_query)
        )
    
    # --- Filter Handling (Modified to use Trim/Lower for consistency) ---
    
    # Get the filter values from the request
    category_filter = request.GET.get('category', '')
    type_filter = request.GET.get('type', '')
    
    # Handle category filter
    if category_filter:
        # To ensure the filter works correctly even if the database has varying case/whitespace,
        # we clean the 'category' field on the fly to match the cleaned category_filter value.
        recipes = recipes.annotate(
            filter_category_field=Trim(Lower('category'))
        ).filter(
            filter_category_field__iexact=category_filter
        )
    
    # Handle type filter
    if type_filter:
        # Apply the same cleaning principle for the type filter
        recipes = recipes.annotate(
            filter_type_field=Trim(Lower('type'))
        ).filter(
            filter_type_field__iexact=type_filter
        )
        
    # --- Dropdown Option Generation (Modified for no duplicates) ---
    
    # Get unique, cleaned categories for filter dropdowns.
    # This prevents duplicates like "Dessert" and " dessert".
    categories_qs = Recipe.objects.annotate(
        cleaned_category=Trim(Lower('category'))
    ).filter(
        # Exclude recipes where the category field is NULL
        category__isnull=False
    ).exclude(
        # Exclude recipes where the cleaned category is an empty string
        cleaned_category=''
    ).order_by(
        'cleaned_category'
    ).values_list(
        'cleaned_category', flat=True
    ).distinct()
    
    # Do the same for types
    types_qs = Recipe.objects.annotate(
        cleaned_type=Trim(Lower('type'))
    ).filter(
        type__isnull=False
    ).exclude(
        cleaned_type=''
    ).order_by(
        'cleaned_type'
    ).values_list(
        'cleaned_type', flat=True
    ).distinct()
    
    # Convert the querysets to lists for the context
    categories = list(categories_qs)
    types = list(types_qs)

    # --- End of Filtering and Dropdown Logic ---

    # Get selected recipe IDs from session
    selected_ids = request.session.get('selected_recipes', [])
    selected_count = len(selected_ids)
    
    context = {
        'recipes': recipes,
        # The cleaning/filtering for NULL/empty values is handled in the queryset, 
        # so the list comprehension [c for c in categories if c] is no longer necessary.
        'categories': categories,
        'types': types,
        'search_query': search_query,
        'category_filter': category_filter,
        'type_filter': type_filter,
        'selected_count': selected_count,
        'page_title': 'CookBook - Recipe Browser'
    }
    
    return render(request, 'CookBook/home.html', context)


def recipe_detail(request, recipe_id):
    """
    Display detailed view of a single recipe
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    context = {
        'recipe': recipe,
        'page_title': f'{recipe.title} - Recipe Details'
    }
    
    return render(request, 'CookBook/recipeDetail.html', context)


@require_http_methods(["POST"])
def select_recipe(request, recipe_id):
    """
    Add recipe to selection (AJAX endpoint)
    """
    selected_recipes = request.session.get('selected_recipes', [])
    
    if recipe_id not in selected_recipes:
        selected_recipes.append(recipe_id)
        request.session['selected_recipes'] = selected_recipes
        request.session.modified = True
    
    return JsonResponse({
        'success': True,
        'selected_count': len(selected_recipes),
        'message': 'Recipe added to selection'
    })


@require_http_methods(["POST"])
def deselect_recipe(request, recipe_id):
    """
    Remove recipe from selection (AJAX endpoint)
    """
    selected_recipes = request.session.get('selected_recipes', [])
    
    if recipe_id in selected_recipes:
        selected_recipes.remove(recipe_id)
        request.session['selected_recipes'] = selected_recipes
        request.session.modified = True
    
    return JsonResponse({
        'success': True,
        'selected_count': len(selected_recipes),
        'message': 'Recipe removed from selection'
    })


@require_http_methods(["POST"])
def generate_grocery_list(request):
    """
    Generate consolidated grocery list from selected recipes
    Consolidates ingredients and removes duplicates
    """
    try:
        data = json.loads(request.body)
        recipe_ids = data.get('recipe_ids', [])
        
        if not recipe_ids:
            return JsonResponse({
                'success': False,
                'message': 'No recipes selected'
            }, status=400)
        
        # Fetch selected recipes
        recipes = Recipe.objects.filter(id__in=recipe_ids)
        
        # Consolidate ingredients
        all_ingredients = set()
        for recipe in recipes:
            if recipe.ingredients:
                for ingredient in recipe.ingredients:
                    # Normalize for comparison but keep original format for display
                    cleaned = ingredient.strip().lower()
                    if cleaned:
                        all_ingredients.add(ingredient.strip())
        
        # Convert set to sorted list
        grocery_list = sorted(list(all_ingredients))
        
        # Store in session for rendering on grocery list page
        request.session['grocery_list'] = grocery_list
        request.session['selected_recipe_ids'] = recipe_ids
        request.session['recipe_count'] = len(recipes)
        
        return JsonResponse({
            'success': True,
            'grocery_list': grocery_list,
            'recipe_count': len(recipes),
            'item_count': len(grocery_list)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


def grocery_list_view(request):
    """
    Display generated grocery list with checkboxes
    """
    grocery_list = request.session.get('grocery_list', [])
    recipe_ids = request.session.get('selected_recipe_ids', [])
    recipe_count = request.session.get('recipe_count', 0)
    
    recipes = Recipe.objects.filter(id__in=recipe_ids)
    
    context = {
        'grocery_list': grocery_list,
        'recipes': recipes,
        'recipe_count': recipe_count,
        'item_count': len(grocery_list),
        'page_title': 'Grocery List - CookBook'
    }
    
    return render(request, 'CookBook/groceryList.html', context)


def selected_recipes_view(request):
    """
    Display selected recipes (for tab view)
    """
    selected_ids = request.session.get('selected_recipes', [])
    selected_recipes = Recipe.objects.filter(id__in=selected_ids)
    
    context = {
        'selected_recipes': selected_recipes,
        'selected_count': len(selected_ids),
        'page_title': 'Selected Recipes - CookBook'
    }
    
    return render(request, 'CookBook/selectedRecipes.html', context)


def api_docs(request):
    """
    Display API documentation page
    Shows available API endpoints and how to use them
    """
    api_endpoints = [
        {
            'name': 'Random Recipe',
            'endpoint': '/api/random/',
            'method': 'GET',
            'description': 'Get a random recipe',
            'example': 'curl -X GET http://localhost:8000/api/random/',
            'response_example': {
                'title': 'Chicken Biryani',
                'type': 'Non-Veg',
                'category': 'Main Course',
                'ingredients': ['500g chicken', '2 cups rice', '...'],
                'method': ['Step 1', 'Step 2', '...'],
                'tips': ['Tip 1', '...']
            }
        }
    ]
    
    context = {
        'api_endpoints': api_endpoints,
        'page_title': 'API Documentation - CookBook'
    }
    
    return render(request, 'CookBook/apiDocs.html', context)


def about(request):
    """
    About page describing the application
    """
    context = {
        'page_title': 'About - CookBook'
    }
    
    return render(request, 'CookBook/about.html', context)


def clear_selection(request):
    """
    Clear all selected recipes
    """
    request.session['selected_recipes'] = []
    request.session['grocery_list'] = []
    request.session['selected_recipe_ids'] = []
    request.session.modified = True
    
    return redirect('CookBook:home')