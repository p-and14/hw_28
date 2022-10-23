# Generated by Django 4.1.2 on 2022-10-18 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_age_alter_user_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, choices=[('m', 'male'), ('f', 'female')], default='m', max_length=1),
        ),
    ]
