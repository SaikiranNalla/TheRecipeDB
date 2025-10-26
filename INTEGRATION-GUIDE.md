# CookBook App - Complete Implementation Guide

## Project Structure

```
TheRecipeDB/
├── manage.py
├── TheRecipeDB/                  # Main project
│   ├── settings.py               # Updated settings
│   ├── urls.py                   # Updated project URLs
│   ├── wsgi.py
│   └── asgi.py
│
├── RecipeAPI/                    # Existing API app
│   ├── models.py                 # Recipe model
│   ├── views.py                  # API views
│   ├── urls.py                   # API URLs
│   ├── serializers.py            # DRF serializers
│   ├── permissions.py            # API permissions
│   ├── admin.py                  # Admin panel
│   ├── recipes.json              # Recipe data
│   └── ...
│
├── cookbook/                     # NEW: Frontend app (this guide)
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── recipe_detail.html
│   │   ├── grocery_list.html
│   │   ├── about.html
│   │   └── api_docs.html         # API documentation page
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── script.js
│   │   └── images/
│   ├── views.py                  # Frontend views
│   ├── urls.py                   # Frontend URLs
│   ├── forms.py                  # Django forms
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                 # Optional: for saving user preferences
│   └── tests.py
│
└── db.sqlite3
```

## URL Mapping Strategy

```
Root (/) → CookBook App (Homepage)
/api/ → API App (API Documentation & Base)
/api/random/ → Random recipe API
/api/recipes/ → All recipes (if implemented)
/admin/ → Django Admin
```

## Color Palette (Dark Mode Compatible)

### Primary Colors
- **Primary Brand Color**: #2E7D32 (Green - Professional, fresh)
- **Accent Color**: #1565C0 (Blue - Trust, reliability)
- **Warning Color**: #F57C00 (Orange - Caution, calls-to-action)

### Background Colors
- **Light Mode Background**: #FFFFFF
- **Light Mode Secondary**: #F5F5F5
- **Dark Mode Background**: #1A1A1A
- **Dark Mode Secondary**: #2D2D2D

### Text Colors
- **Light Mode Text**: #212121
- **Light Mode Secondary Text**: #757575
- **Dark Mode Text**: #E0E0E0
- **Dark Mode Secondary Text**: #B0B0B0

## File Structure Guide

This guide will walk you through creating:
1. `views.py` - Frontend views
2. `urls.py` - URL routing
3. `forms.py` - Search and filter forms
4. `admin.py` - Admin configuration
5. `templates/` - All HTML files
6. `static/css/style.css` - Custom styling
7. `static/js/script.js` - Frontend JavaScript

---

## Step 1: Create the CookBook App

```bash
python manage.py startapp cookbook
```

## Step 2: Add App to INSTALLED_APPS

In `TheRecipeDB/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'RecipeAPI',              # Existing API app
    'cookbook',               # NEW: Add this
]

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'cookbook' / 'templates'],  # Add this line
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

## Step 3: Update Project URLs

In `TheRecipeDB/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # CookBook App (Main Frontend) - Root paths
    path('', include('cookbook.urls')),
    
    # API endpoints
    path('api/', include('RecipeAPI.urls')),
    
    # Django Admin
    path('admin/', admin.site.urls),
]
```

## Step 4: Create Directory Structure

```bash
# Create template and static directories
mkdir -p cookbook/templates/cookbook
mkdir -p cookbook/static/css
mkdir -p cookbook/static/js
mkdir -p cookbook/static/images
```

## Step 5: Copy All Code Files

Copy the files from next sections into appropriate locations.

---

## Step 6: Create Directory Structure

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: `http://localhost:8000/`

---

## Integration Notes

### Fixing Admin Page

The admin page is used to add recipes. Ensure:
1. Recipe model is registered in `RecipeAPI/admin.py`
2. Use JSON field editors in Django admin
3. Access at `/admin/` with superuser credentials

### API Integration

- CookBook app (frontend) fetches recipes from RecipeAPI (backend)
- Both apps share the same Recipe model from RecipeAPI
- API responses are consumed via AJAX in frontend JavaScript

### Database Considerations

- Both apps use the same database
- Recipe model lives in RecipeAPI app
- CookBook app displays recipes, doesn't store them
- Session-based grocery list storage (no database needed)

---

See detailed files in the next sections for complete implementation.
