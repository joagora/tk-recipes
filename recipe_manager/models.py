# models.py
from django.db import models

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100)
    instructions = models.TextField()

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
