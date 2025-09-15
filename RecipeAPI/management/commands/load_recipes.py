import json
from django.core.management.base import BaseCommand
from RecipeAPI.models import Recipe # Replace RecipeAPI with your app name

class Command(BaseCommand):
    help = 'Loads recipe data from a JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file to load.')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found at: {json_file}'))
            return
            
        recipes_data = data.get('recipes', {})
        if not recipes_data:
            self.stdout.write(self.style.WARNING('No "recipes" key found in the JSON data.'))
            return

        for title, recipe_details in recipes_data.items():
            # Check if a recipe with the same title already exists
            if not Recipe.objects.filter(title=title).exists():
                try:
                    Recipe.objects.create(
                        title=title,
                        ingredients=recipe_details.get('ingredients', []),
                        method=recipe_details.get('method', []),
                        tips=recipe_details.get('tips', []),
                        category=recipe_details.get('category', None),
                        # Note: The 'type' field is not in your JSON, so we will not include it here
                        # It will be set to its default value (None in this case)
                    )
                    self.stdout.write(self.style.SUCCESS(f'Successfully added recipe: {title}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to add recipe {title}: {e}'))
            else:
                self.stdout.write(self.style.WARNING(f'Recipe already exists, skipping: {title}'))

        self.stdout.write(self.style.SUCCESS('Data loading complete.'))
