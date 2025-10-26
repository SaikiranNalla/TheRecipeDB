# PROJECT REPORT

**Project Title:** Recipe Grocery List Generator

**A Dissertation Submitted in Partial Fulfilment of the Requirements**
for the award of degree of Master of Computer Applications (M.C.A.)


---

## Certificate

This is to certify that the project report entitled **Recipe Grocery List Generator** submitted by **[Student Name]**, Registration No. ___________, in partial fulfilment of the requirements for the award of the degree of Master of Computer Applications (M.C.A.), Osmania University, is a record of bonafide work carried out by him/her under my supervision. The results embodied in this report have not been submitted to any other institution or university for any other degree or diploma.


_**Place:** Hyderabad &nbsp;&nbsp;&nbsp;&nbsp; **Date:** ___________


**Signature of Guide**

_Guide Name, Assistant Professor, Dept. of Computer Science & Engineering, University College of Engineering, Osmania University, Hyderabad_

---

## Declaration

I hereby declare that the project work reported in this report titled **Recipe Grocery List Generator** is an original work carried out by me under the guidance of **Guide Name**, Assistant Professor, Department of Computer Science and Engineering, University College of Engineering, Osmania University, Hyderabad. I further declare that this report has not been submitted to any other university or institution for the award of any degree or diploma.


_**Place:** Hyderabad &nbsp;&nbsp;&nbsp;&nbsp; **Date:** ___________

_**Student Name**, Reg. No. ________, M.C.A. PGRRCDE, Osmania University_

---

## Acknowledgements

I express my sincere gratitude to my project guide, **Guide Name**, for his/her invaluable guidance and constant encouragement throughout this project. I would like to thank the Department of Computer Science and Engineering for providing infrastructure and resources. I am also thankful to my peers and family for their support and cooperation.

---

## Abstract

The **Recipe Grocery List Generator** application simplifies the process of creating grocery lists from chosen recipes. It allows users to select recipes from a comprehensive list, view selected recipes, and generate a consolidated grocery list with unique ingredients. The system is built with **Django** (backend), **HTML/CSS/Bootstrap** (frontend), and **PostgreSQL** via **Supabase** for data storage. The application addresses the common issue of forgetting ingredients and duplicate items by providing a tick-box grocery list. This report details the high-level and low-level design, implementation, database schema, user interface, and instructions to run the application.

---

## Table of Contents

1. Introduction
2. High-Level Design
3. Low-Level Design
4. Implementation
   - Frontend
   - Backend
   - Database
5. Models Update
6. User Interface
7. Readme and Deployment
8. Conclusion
9. References

---

## 1. Introduction

The **Recipe Grocery List Generator** aims to streamline meal planning by allowing users to generate grocery lists directly from selected recipes. Users interact with a homepage listing all recipes and a tab showing selected recipes. By clicking "Generate Grocery List," users receive a consolidated list of ingredients with tick boxes to mark items purchased. This functionality reduces the cognitive load in meal preparation and avoids missing or duplicate grocery items.

## 2. High-Level Design

The system follows a three-tier architecture:

- **Presentation Tier:** HTML/CSS/Bootstrap front-end renders recipe lists and grocery list interface.
- **Logic Tier:** Django views and REST APIs handle user requests, recipe selection, and grocery list generation.
- **Data Tier:** PostgreSQL database (hosted on Supabase) stores recipes in JSON fields and user data.

A common navbar is included on all pages with options: Home, About, Admin, and Dark Mode toggle (Bootstrap built-in).

## 3. Low-Level Design

### 3.1 Models

The existing **Recipe** model uses JSONFields for `ingredients`, `method`, and `tips`. No additional models are required unless user accounts or grocery list persistence is needed. For persisting grocery lists, an optional **GroceryList** model can be introduced:

```python
class GroceryList(models.Model):
    recipes = models.ManyToManyField(Recipe)
    created_at = models.DateTimeField(auto_now_add=True)
    items = JSONField()  # list of unique ingredients
```

### 3.2 Views and URLs

- **HomeView:** Lists all recipes and selected recipes tabs.
- **GenerateGroceryListView:** Accepts selected recipe IDs, aggregates ingredients, removes duplicates, returns JSON.

### 3.3 API Endpoints

- `/api/recipes/` [GET]
- `/api/recipes/selected/` [POST, GET]
- `/api/grocery-list/generate/` [POST]

## 4. Implementation

### 4.1 Frontend

- **HTML/CSS/Bootstrap:** Responsive layout with two tabs. Use Bootstrap nav-pills for tabbed navigation. Grocery list with `<ul>` of `<li><input type="checkbox"> ingredient`.

### 4.2 Backend

- **Django:** Use Django REST Framework for APIs. Views handle JSON input/output.
- **Data Ingestion:** Recipe data loaded via AI chatbot from PDF, stored as JSON in `Recipe` model. Alternatively, use management command to parse structured JSON files.

### 4.3 Database

- **PostgreSQL (Supabase):** Stores `Recipe` and optional `GroceryList` tables. Ensure `JSONField` enabled.

## 5. Models Update

If persisting grocery lists, add **GroceryList** model as described in Low-Level Design. Otherwise, current `Recipe` model suffices.

## 6. User Interface

Common navbar in `base.html` with links: Home, About, Admin, Dark Mode toggle. Two tabs on homepage: All Recipes, Selected Recipes. Grocery list page displays tick-box ingredients and a "Download List" button.

## 7. Readme and Deployment

### 7.1 Purpose

This application eases grocery list generation from recipes, minimizing missing or duplicate items.

### 7.2 Requirements

- Python 3.9+
- Django 4.x
- Django REST Framework
- psycopg2
- Bootstrap 5
- Supabase account

### 7.3 Setup

1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `DATABASE_URL` in `.env` pointing to Supabase
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Load recipe data: `python manage.py loaddata recipes.json`
7. Run server: `python manage.py runserver`

### 7.4 Usage

- Access `http://localhost:8000/` for homepage.
- Use admin panel to add/edit recipes.
- Select recipes and click "Generate Grocery List".

## 8. Conclusion

The **Recipe Grocery List Generator** provides a user-friendly interface to select recipes and automatically generate grocery lists. The modular design supports easy extension, such as user accounts and grocery list history. The application leverages Django and Supabase for robust backend support and Bootstrap for responsive frontend design.

## 9. References

- Osmania University project format guidelines
- Django documentation

