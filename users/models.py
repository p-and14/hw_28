from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import validators

from users.validators import AgeMinValidator, EmailNotAllowValidator


class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
        ordering = ["id"]

    def __str__(self):
        return self.name


class User(AbstractUser):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLES = [
        (MEMBER, "пользователь"),
        (MODERATOR, "модератор"),
        (ADMIN, "админ"),
    ]

    MALE = "m"
    FEMALE = "f"
    SEX = [(MALE, "male"), (FEMALE, "female")]

    role = models.CharField(max_length=10, choices=ROLES, default="member")
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="user", null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX, default=MALE, blank=True)
    birth_date = models.DateField(validators=[AgeMinValidator(9)])
    email = models.CharField(
        max_length=30,
        unique=True,
        validators=[validators.EmailValidator(), EmailNotAllowValidator("rambler.ru")])

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username
