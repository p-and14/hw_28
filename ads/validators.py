from rest_framework import exceptions


def is_published_not_true(value):
    if value:
        raise exceptions.ValidationError("Значение поля при создании объявления не может быть True")
