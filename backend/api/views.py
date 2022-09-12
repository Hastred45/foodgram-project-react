from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from fpdf import FPDF
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.filters import RecipeFilter
from recipes.models import Favorite, IngredientAmount, Recipe, ShoppingCart
from recipes.permissions import AuthorOrReadOnly
from recipes.serializers import RecipeSerializer, SmallRecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add(self, model, user, pk, name):
        """Добавление рецепта в список пользователя."""
        recipe = get_object_or_404(Recipe, pk=pk)
        relation = model.objects.filter(user=user, recipe=recipe)
        if relation.exists():
            return Response(
                {'errors': f'Нельзя повторно добавить рецепт в {name}'},
                status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user, recipe=recipe)
        serializer = SmallRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_relation(self, model, user, pk, name):
        """"Удаление рецепта из списка пользователя."""
        recipe = get_object_or_404(Recipe, pk=pk)
        relation = model.objects.filter(user=user, recipe=recipe)
        if not relation.exists():
            return Response(
                {'errors': f'Нельзя повторно удалить рецепт из {name}'},
                status=status.HTTP_400_BAD_REQUEST)
        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True, url_path='favorite',
            url_name='favorite')
    def favorite(self, request, pk=None):
        """Добавление и удаление рецептов - Избранное."""
        user = request.user
        if request.method == 'POST':
            name = 'избранное'
            return self.add(Favorite, user, pk, name)
        if request.method == 'DELETE':
            name = 'избранного'
            return self.delete_relation(Favorite, user, pk, name)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['post', 'delete'], detail=True, url_path='shopping_cart',
            url_name='shopping_cart')
    def shopping_cart(self, request, pk=None):
        """Добавление и удаление рецептов - Список покупок."""
        user = request.user
        if request.method == 'POST':
            name = 'список покупок'
            return self.add(ShoppingCart, user, pk, name)
        if request.method == 'DELETE':
            name = 'списка покупок'
            return self.delete_relation(ShoppingCart, user, pk, name)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['get'], detail=False, url_path='download_shopping_cart',
            url_name='download_shopping_cart')
    def download_cart(self, request):
        """Формирование и скачивание списка покупок."""
        user = request.user
        ingredients = IngredientAmount.objects.filter(
            recipe__sh_cart__user=user).values(
                'ingredient__name', 'ingredient__measurement_unit').annotate(
                    Sum('amount', distinct=True))
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font(
            'DejaVu', '', './recipes/fonts/DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', size=14)
        pdf.cell(txt='Список покупок', center=True)
        pdf.ln(8)
        for i, ingredient in enumerate(ingredients):
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['amount__sum']
            pdf.cell(40, 10, f'{i + 1}) {name} - {amount} {unit}')
            pdf.ln()
        file = pdf.output(dest='S')
        response = HttpResponse(
            content_type='application/pdf', status=status.HTTP_200_OK)
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.pdf"')
        response.write(bytes(file))
        return response
