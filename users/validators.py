from datetime import date

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class AgeMinValidator:
    def __init__(self, age):
        self.age = age

    def __call__(self, value):
        today = date.today()
        try:
            birthday = value.replace(year=today.year)
        except ValueError:
            birthday = value.replace(year=today.year, month=value.month + 1, day=1)
        if birthday > today:
            age = today.year - value.year - 1
        else:
            age = today.year - value.year

        if age < self.age:
            raise ValidationError("Пользователям младше 9 лет запрещено регистрироваться")


@deconstructible
class EmailNotAllowValidator:
    def __init__(self, emails):
        if not isinstance(emails, list):
            emails = [emails]
        self.emails = emails

    def __call__(self, value):
        email_part = value.split("@")[-1]

        if email_part in self.emails:
            raise ValidationError(f"Запрещена регистрация с почтового адреса в домене {email_part}")
