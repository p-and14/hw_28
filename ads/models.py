from django.db import models

from users.models import User


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='', verbose_name="Имя")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ad", verbose_name="Автор")
    price = models.IntegerField(verbose_name="Цена")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    image = models.ImageField(upload_to="images/", verbose_name="Фото")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="ad", verbose_name="Категория")

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Selection(models.Model):
    name = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="selection", verbose_name="Владелец")
    items = models.ManyToManyField(Ad, related_name="selection")

    class Meta:
        verbose_name = "Подборка объявлений"
        verbose_name_plural = "Подборки объявлений"

    def __str__(self):
        return self.name
