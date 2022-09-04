from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        max_length=7,
        unique=True
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Только латинские буквы и символы "-" "_"',
            ),
        ]
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name
