from django.test import TestCase
from django.urls import reverse
from .models import Ingredient, Recipe
import json



class RecipeTestCase(TestCase):

        
    def test_create_recipe(self):
            """
            Posting creates a new recipe with ingredients.
            """
        
            # Data for creating a recipe
            data = {
                "recipe_name": "Pizza",
                "instructions": "Put it in the oven",
                "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
            }

            response = self.client.post(reverse('recipe-create'), json.dumps(data), content_type="application/json",) 

            self.assertEqual(response.status_code, 201)


            recipes = Recipe.objects.all()
            self.assertEqual(len(recipes), 1)

            recipe = recipes[0]

            self.assertEqual(recipe.recipe_name, data['recipe_name'])
            self.assertEqual(recipe.instructions, data['instructions'])

            ingredients_count = recipe.ingredients.count()
            self.assertEqual(ingredients_count, len(data['ingredients']))
    
    def test_update_recipe(self):
            """
                Put updates the values correctly
            """
        
            # arrange
            updated_name = "Test name"
            updated_ingredients =  [{"name": "test ingredient"}]

            data = {
                "recipe_name": "Pizza",
                "instructions": "Put it in the oven",
                "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
            }

            self.client.post(reverse('recipe-create'), json.dumps(data), content_type="application/json",) 
            recipes = Recipe.objects.all()
            recipe = recipes[0]

            data['recipe_name'] = updated_name
            data["ingredients"] = updated_ingredients

            # act
            url = reverse('recipe-update', kwargs={'pk': recipe.id})

            response = self.client.put(url, json.dumps(data), content_type="application/json") 

            # assert
            self.assertEqual(response.status_code, 200)


            self.assertEqual(len(recipes), 1)

            recipes = Recipe.objects.all()
            recipe = recipes[0]


            self.assertEqual(recipe.recipe_name, updated_name)
            self.assertEqual(recipe.ingredients.first().name, updated_ingredients[0]['name'])

            ingredients_count = recipe.ingredients.count()
            self.assertEqual(ingredients_count, len(updated_ingredients))
        
    def test_get_recipe_list(self):
            """
            Getting recipe list with ingredients.
            """
        
            # arrange
            data = {
                "recipe_name": "Pizza",
                "instructions": "Put it in the oven",
                "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
            }

            response = self.client.post(reverse('recipe-create'), json.dumps(data), content_type="application/json",) 

            self.assertEqual(response.status_code, 201)


            recipes = Recipe.objects.all()
            self.assertEqual(len(recipes), 1)

            # act
            response = self.client.get(reverse('recipe-list')) 

            # assert
            self.assertEqual(len(response.data ), 1)

    def test_get_recipe(self):
            """
            Getting recipe list with ingredients.
            """
        
            # arrange
            recipe_1 = {
                "recipe_name": "Pizza",
                "instructions": "Put it in the oven",
                "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
            }

            recipe_2 = {
                "recipe_name": "Carbonara",
                "instructions": "Cook pasta and don't add cream!",
                "ingredients": [{"name": "pasta"}, {"name": "parmesan"}, {"name": "bacon"}]
            }

            self.client.post(reverse('recipe-create'), json.dumps(recipe_1), content_type="application/json",) 
            self.client.post(reverse('recipe-create'), json.dumps(recipe_2), content_type="application/json",) 

            recipes = Recipe.objects.all()
            self.assertEqual(len(recipes), 2)

            url = reverse('recipe-retrieve', kwargs={'pk': 1})

            # act
            response = self.client.get(url) 

            # assert
            recipe = response.data

            self.assertEqual(recipe['recipe_name'], recipe_1['recipe_name'])
            
    def test_delete_recipe(self):
            """
            Delete removes the recipe and ingredients
            """
        
            # arrange
            data = {
                "recipe_name": "Pizza",
                "instructions": "Put it in the oven",
                "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
            }

            response = self.client.post(reverse('recipe-create'), json.dumps(data), content_type="application/json",) 

            self.assertEqual(response.status_code, 201)


            recipes = Recipe.objects.all()
            self.assertEqual(len(recipes), 1)
            recipe = recipes[0]

            url = reverse('recipe-destroy', kwargs={'pk': recipe.id})

            # act
            response = self.client.delete(url) 

            # assert
            recipes = Recipe.objects.all()
            self.assertEqual(len(recipes), 0)

            ingredients = Ingredient.objects.all()
            self.assertEqual(len(ingredients), 0)


    def test_search_recipe_by_full_name(self):
            """
            Searching recipe.
            """
        
            # arrange
            recipe_1 = {
                "recipe_name": "Pizza",
                "instructions": "Put it in the oven",
                "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
            }

            recipe_2 = {
                "recipe_name": "Carbonara",
                "instructions": "Cook pasta and don't add cream!",
                "ingredients": [{"name": "pasta"}, {"name": "parmesan"}, {"name": "bacon"}]
            }

            self.client.post(reverse('recipe-create'), json.dumps(recipe_1), content_type="application/json",) 
            self.client.post(reverse('recipe-create'), json.dumps(recipe_2), content_type="application/json",) 

            recipes = Recipe.objects.all()
            self.assertEqual(len(recipes), 2)

            url = reverse('recipe-search-by-name') + '?name=Pizza'

            # act
            response = self.client.get(url) 

            # assert
            search_result = response.data

            self.assertEqual(len(search_result), 1)
            self.assertEqual(search_result[0]['recipe_name'], "Pizza")
            
    def test_search_recipe_by_partial_name(self):
            """
            Searching recipe by partial name.
            """
        
            # arrange
            recipe_1 = {
                "recipe_name": "Pizza",
                "instructions": "Put it in the oven",
                "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
            }

            recipe_2 = {
                "recipe_name": "Carbonara",
                "instructions": "Cook pasta and don't add cream!",
                "ingredients": [{"name": "pasta"}, {"name": "parmesan"}, {"name": "bacon"}]
            }

            self.client.post(reverse('recipe-create'), json.dumps(recipe_1), content_type="application/json",) 
            self.client.post(reverse('recipe-create'), json.dumps(recipe_2), content_type="application/json",) 

            recipes = Recipe.objects.all()
            self.assertEqual(len(recipes), 2)

            url = reverse('recipe-search-by-name') + '?name=Pi'

            # act
            response = self.client.get(url) 

            # assert
            search_result = response.data

            self.assertEqual(len(search_result), 1)
            self.assertEqual(search_result[0]['recipe_name'], "Pizza")
            