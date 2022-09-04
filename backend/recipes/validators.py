from rest_framework.validators import ValidationError as RFError

from tags_ingr.models import Ingredient, Tag


def validate_time(value):
    """Валидация поля модели - время приготовления."""
    if value < 1:
        raise RFError(
            ['Время не может быть менее минуты.']
        )


def validate_ingredients(data):
    """Валидация ингредиентов и количества."""
    if not data:
        raise RFError({'ingredients': ['Обязательное поле.']})
    if len(data) < 1:
        raise RFError({'ingredients': ['Не переданы ингредиенты.']})
    unique_ingredient = []
    for ingredient in data:
        if not ingredient.get('id'):
            raise RFError({'ingredients': ['Отсутствует id ингредиента.']})
        id = ingredient.get('id')
        if not Ingredient.objects.filter(id=id).exists():
            raise RFError({'ingredients': ['Ингредиента нет в БД.']})
        if id in unique_ingredient:
            raise RFError(
                {'ingredients': ['Нельзя дублировать имена ингредиентов.']})
        unique_ingredient.append(id)
        amount = int(ingredient.get('amount'))
        if amount < 1:
            raise RFError({'amount': ['Количество не может быть менее 1.']})
    return data


def validate_tags(data):
    """Валидация тэгов: отсутствие в request, отсутствие в БД."""
    if not data:
        raise RFError({'tags': ['Обязательное поле.']})
    if len(data) < 1:
        raise RFError({'tags': ['Хотя бы один тэг должен быть указан.']})
    for tag in data:
        if not Tag.objects.filter(id=tag).exists():
            raise RFError({'tags': ['Тэг отсутствует в БД.']})
    return data
