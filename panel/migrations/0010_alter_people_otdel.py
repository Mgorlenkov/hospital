# Generated by Django 3.2.9 on 2021-11-24 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0009_people_otdel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='otdel',
            field=models.CharField(blank=True, choices=[('1', '1-ое отделение'), ('2', '2-ое отделение'), ('3', '3-ое отделение')], max_length=50, verbose_name='Отделение'),
        ),
    ]
