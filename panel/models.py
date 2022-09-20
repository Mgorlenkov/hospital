from django.db import models
from django.contrib.admin.helpers import ActionForm
from django.conf import settings


class Otdel(models.Model):

    name = models.TextField(verbose_name = "Полное название")
    short_name = models.TextField(verbose_name = "Короткое название")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otdel = models.ForeignKey(Otdel, on_delete=models.CASCADE)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class People(models.Model):

    name = models.TextField(verbose_name = "ФИО")
    nIb = models.TextField(verbose_name = "№ИБ")
    room = models.BigIntegerField(verbose_name = "№ палаты")
    date = models.TextField(verbose_name = "Дата госпитализации")
    otdel = models.ForeignKey(Otdel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Список пациентов'
        verbose_name_plural = 'Список пациентов'