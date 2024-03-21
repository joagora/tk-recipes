from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from .models import Recipe
from .serializers import RecipeSerializer

# List view
class RecipeListView(ListAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

# Create view
class RecipeCreateView(CreateAPIView):
    serializer_class = RecipeSerializer

# Retrieve view
class RecipeRetrieveView(RetrieveAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

# Update view
class RecipeUpdateView(UpdateAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

# Destroy view
class RecipeDeleteView(DestroyAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

# Seach recipe
class RecipeSearchByName(ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            return Recipe.objects.filter(recipe_name__icontains=name)
        else:
            return Recipe.objects.none()  # Return an empty queryset if no name is provided
