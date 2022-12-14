# Generated by Django 3.2.9 on 2021-11-25 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0010_alter_people_otdel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Otdel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='ФИО')),
                ('short_name', models.TextField(verbose_name='ФИО')),
            ],
            options={
                'verbose_name': 'Отдел',
                'verbose_name_plural': 'Отделы',
            },
        ),
        migrations.AlterField(
            model_name='people',
            name='otdel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.otdel'),
        ),
    ]
