from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Favorite, IngredientAmount, Recipe, ShoppingCart
from recipes.validators import validate_ingredients, validate_tags
from tags_ingr.models import Ingredient, Tag
from tags_ingr.serializers import TagSerializer
from users.serializers import CustomUserSerializer


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = (
            'id', 'name', 'measurement_unit', 'amount'
        )


class SmallRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientAmountSerializer(
        read_only=True, many=True, source='ingredientamount_set')
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        """Статус - рецепт в избранном или нет."""
        user_id = self.context.get('request').user.id
        return Favorite.objects.filter(
            user=user_id, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        """Статус - рецепт в избранном или нет."""
        user_id = self.context.get('request').user.id
        return ShoppingCart.objects.filter(
            user=user_id, recipe=obj.id).exists()

    def create_ingredient_amount(self, valid_ingredients, recipe):
        """Создание уникальных записей: ингредиент - рецепт - количество."""
        for ingredient_data in valid_ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=ingredient_data.get('id'))
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=ingredient_data.get('amount'))

    def create_tags(self, data, recipe):
        """Отправка на валидацию и создание тэгов у рецепта."""
        valid_tags = validate_tags(data.get('tags'))
        tags = Tag.objects.filter(id__in=valid_tags)
        recipe.tags.set(tags)

    def create(self, validated_data):
        """Создание рецепта - writable nested serializers."""
        valid_ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_tags(self.initial_data, recipe)
        self.create_ingredient_amount(valid_ingredients, recipe)
        return recipe

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        valid_ingredients = validate_ingredients(ingredients)
        data['ingredients'] = valid_ingredients
        return data

    def update(self, instance, validated_data):
        """Изменение рецепта - writable nested serializers."""
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        instance.tags.remove()
        self.create_tags(self.initial_data, instance)
        instance.ingredientamount_set.filter(recipe__in=[instance.id]).delete()
        valid_ingredients = validated_data.get(
            'ingredients', instance.ingredients)
        self.create_ingredient_amount(valid_ingredients, instance)
        return instance
