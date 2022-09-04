from rest_framework import viewsets

from tags_ingr.filters import CustomSearchFilter
from tags_ingr.models import Ingredient, Tag
from tags_ingr.serializers import IngredientSerializer, TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [CustomSearchFilter]
    search_fields = ('^name',)
