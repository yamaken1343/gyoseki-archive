from django.core.validators import FileExtensionValidator
from django.db import models


def get_upload_to(instance, filename):
    print(instance.date.strftime("%Y/%m/%d") + str(instance.main_author) + str(instance.division))
    return str(
        instance.date.strftime("%Y-%m-%d") + "_" + str(instance.main_author) + "_" + str(instance.division) + str(
            instance.title)[:8]) + '.pdf'

# Create your models here.
from django import forms


class Author(models.Model):
    name = models.CharField(max_length=128, unique=True)
    en_name = models.CharField(max_length=128)
    joined_at = models.DateField()
    quited_at = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=128)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Division(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Recode(models.Model):
    main_author = models.ForeignKey('Author', on_delete=models.PROTECT)  # 主著者
    author = models.CharField(max_length=256)  # 著者
    en_author = models.CharField(max_length=256, null=True, blank=True)  # 著者(英)
    title = models.CharField(max_length=256)
    en_title = models.CharField(max_length=256, null=True, blank=True)
    journal = models.CharField(max_length=256, null=True, blank=True)  # 雑誌名, 学会名等
    en_journal = models.CharField(max_length=256, null=True, blank=True)
    vol = models.CharField(max_length=256, null=True, blank=True)
    no = models.CharField(max_length=256, null=True, blank=True)
    page = models.CharField(max_length=256, null=True, blank=True)
    date = models.DateField()
    language = models.ForeignKey('Language', on_delete=models.PROTECT, null=True, blank=True)
    division = models.ForeignKey('Division', on_delete=models.PROTECT, null=True, blank=True)  # 業績区分
    place = models.CharField(max_length=128, null=True, blank=True)
    en_place = models.CharField(max_length=128, null=True, blank=True)
    tag = models.ManyToManyField('Tag', blank=True)
    review = models.BooleanField(null=True, blank=True)  # 査読の有無
    note = models.TextField(null=True, blank=True)  # 備考
    file = models.FileField(upload_to=get_upload_to, null=True, blank=True)

    def __str__(self):
        return self.title
