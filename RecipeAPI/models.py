from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import json
from django.db.models import JSONField, Model, CharField


# Create your models here.
# class UserManager(BaseUserManager):
#     """Manager for users"""
#     def create_user(self, name, email, password=None):
#         """Create, save and return a new user"""
#         if not email:
#             raise ValueError('User must have an email address')

#         email = self.normalize_email(email)
#         user = self.model(email=email, name=name)

#         user.set_password(password)
#         user.save(using=self._db)

#         return user

#     def create_superuser(self, name, email, password):
#         """Create and return a new superuser"""
#         user = self.create_user(name, email, password)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)

#         return user

# class UserProfile(AbstractBaseUser, PermissionsMixin):
#     """Database model for users in the system"""
#     email = models.EmailField(max_length=255, unique=True)
#     name = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']

#     objects = UserManager()

#     def get_full_name(self):
#         """Retrieve full name of user"""
#         return self.name

#     def get_short_name(self):
#         return self.name

#     def __str__(self):
#         """Return string representation of our user"""
#         return self.email


TYPE_CHOICES = [
    ("Veg", "Veg"),
    ("Non-Veg", "Non-Veg"),
    ("Vegan", "Vegan"),
    ("Eggiterian", "Eggiterian"),
]

class Recipe(models.Model):

    title = models.CharField(max_length=255, db_index=True) 
    alt_names = JSONField(blank=True, null=True, default=list)
    ingredients = JSONField(blank=True, null=True, default=list)
    method = JSONField(blank=True, null=True, default=list)
    tips = JSONField(blank=True, null=True, default=list)
    category = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, blank=True, null=True)



    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['alt_names']),
        ]

    def save(self, *args, **kwargs):
        if not self.alt_names:
            self.alt_names = [self.title]
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.title



