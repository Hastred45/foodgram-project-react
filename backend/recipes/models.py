from django.core.validators import MinValueValidator
from django.db import models

from recipes.validators import validate_time
from tags_ingr.models import Ingredient, Tag
from users.models import User


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name='recipes')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientAmount'
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/'
    )
    text = models.TextField()
    cooking_time = models.IntegerField(validators=[validate_time])

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, 'Не может быть менее 1')]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite_recipe'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sh_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='sh_cart'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_cart_recipe'
            )
        ]
