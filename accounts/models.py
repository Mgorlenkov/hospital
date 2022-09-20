from django.db import models

class GlikProfileModel(models.Model):

    name = models.TextField(verbose_name = "ФИО")
    date = models.DateField(verbose_name = "дата")
    room = models.TextField(verbose_name = "№ палаты")

    class Meta:
        verbose_name = 'Глик профиль'
        verbose_name_plural = 'Глик профиль'


class PinList(models.Model):

    name = models.TextField(verbose_name = "ФИО")
    date = models.DateField(verbose_name = "дата")
    med = models.TextField(verbose_name="мед сестра")
    doctor = models.TextField(verbose_name="врач")
    pvk_date = models.DateField(verbose_name = "дата pvk")
    zvk_date = models.DateField(verbose_name = "дата zvk")
    uk_date = models.DateField(verbose_name = "дата uk")
    diabet = models.BooleanField(verbose_name="chekbox")
    lite = models.BooleanField(verbose_name="chekbox")
    belok = models.BooleanField(verbose_name="chekbox")
    lite_belok = models.BooleanField(verbose_name="chekbox")
    low_kallory = models.BooleanField(verbose_name="chekbox")
    hight_kallory = models.BooleanField(verbose_name="chekbox")
    yes_no = models.BooleanField(verbose_name="chekbox")
    n = models.BooleanField(verbose_name="chekbox")
    one = models.BooleanField(verbose_name="chekbox")
    two = models.BooleanField(verbose_name="chekbox")
    chair = models.BooleanField(verbose_name="chekbox")
    deadline = models.DateField(verbose_name = "дата")


    class Meta:
        verbose_name = 'пин лист'
        verbose_name_plural = 'пин листы'


class ExcelInput(models.Model):

    file_in = models.FileField(verbose_name="EXCEL список пациентов")

    class Meta:
        verbose_name = 'ExcelInput'
        verbose_name_plural = 'ExcelInputs'
