# serializers.py
from rest_framework import serializers
from .models import Recipe, Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'recipe_name', 'instructions', 'ingredients']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe
    
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')

        # Update recipe fields
        instance.recipe_name = validated_data.get('recipe_name', instance.recipe_name)
        instance.instructions = validated_data.get('instructions', instance.instructions)
        instance.save()

        # Update ingredients
        ingredient_ids = [ingredient_data.get('id') for ingredient_data in ingredients_data]
        # Delete ingredients not in the update data
        instance.ingredients.exclude(id__in=ingredient_ids).delete()
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            if ingredient_id:
                ingredient = Ingredient.objects.get(id=ingredient_id, recipe=instance)
                ingredient.name = ingredient_data.get('name', ingredient.name)
                ingredient.save()
            else:
                Ingredient.objects.create(recipe=instance, **ingredient_data)

        return instance