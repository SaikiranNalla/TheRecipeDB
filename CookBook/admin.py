from django.contrib import admin

# Register your models here.
from django.contrib import admin
from RecipeAPI.models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing recipes
    Use this page to add, edit, or delete recipes
    """
    list_display = ('title', 'type', 'category', 'ingredients_count')
    list_filter = ('type', 'category')
    search_fields = ('title', 'alt_names', 'category')
    ordering = ('title',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'alt_names', 'category', 'type'),
            'description': 'Enter the recipe name, alternative names, and classification'
        }),
        ('Recipe Details', {
            'fields': ('ingredients', 'method', 'tips'),
            'description': 'Enter ingredients as JSON list, cooking method steps, and chef tips'
        }),
    )
    
    readonly_fields = ('ingredients_count',)
    
    def ingredients_count(self, obj):
        """Display count of ingredients"""
        return len(obj.ingredients) if obj.ingredients else 0
    
    ingredients_count.short_description = 'Number of Ingredients'
    
    def get_queryset(self, request):
        """Order recipes by title by default"""
        qs = super().get_queryset(request)
        return qs.order_by('title')


# Admin site customization
admin.site.site_header = "CookBook Administration"
admin.site.site_title = "CookBook Admin"
admin.site.index_title = "Welcome to CookBook Administration"