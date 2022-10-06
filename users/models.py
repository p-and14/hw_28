from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
        ordering = ["id"]

    def __str__(self):
        return self.name


class User(models.Model):
    ROLES = [
        ("member", "пользователь"),
        ("moderator", "модератор"),
        ("admin", "админ"),
    ]

    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15, blank=True, default="")
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=10, choices=ROLES, default="member")
    age = models.PositiveSmallIntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username

