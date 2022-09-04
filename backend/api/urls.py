from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import RecipeViewSet
from tags_ingr.views import IngredientViewSet, TagViewSet
from users.views import CustomUserViewSet

app_name = 'api'
router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
