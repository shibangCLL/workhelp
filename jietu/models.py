import os
import uuid

from django.db import models
from users.models import UserInfo


# Create your models here.
def jietu_directory_path(instance, filename):
    filename = instance.domain.name + '.png'
    print(str(instance.domain.expiration_date))
    # return the whole path to the file
    return os.path.join('images', "jietu", str(instance.domain.expiration_date), filename)


class DoaminType(models.Model):
    domaintype = models.CharField('域名类型', max_length=32, null=True, blank=True)

    def __str__(self):
        return self.domaintype

    class Meta:
        verbose_name = '域名类型'
        verbose_name_plural = verbose_name
        ordering = ['-domaintype']


class DoaminExpirationDate(models.Model):
    expiration_date = models.DateField('域名过期时间', unique=True)

    def __str__(self):
        return self.expiration_date.strftime('%Y-%m-%d')

    class Meta:
        verbose_name = '域名过期时间'
        verbose_name_plural = verbose_name


class Doamin(models.Model):
    name = models.CharField('域名', max_length=200, null=True, blank=True, unique=True)
    expiration_date = models.ForeignKey(DoaminExpirationDate, verbose_name='域名过期时间', on_delete=models.CASCADE,
                                        blank=True, null=True)
    user = models.ManyToManyField(UserInfo, verbose_name='域名归属', blank=True, null=True)
    domaintype = models.ForeignKey(DoaminType, verbose_name='域名类型', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField('是否截图', default=False, max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '域名'
        verbose_name_plural = verbose_name
        ordering = ['-name']


class Jietu(models.Model):
    domain = models.OneToOneField(Doamin, verbose_name='域名', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField('域名图片', upload_to=jietu_directory_path)
    views = models.IntegerField('阅览量', default=0)
    content = models.TextField('网站内容', blank=True, null=True)

    def __str__(self):
        return self.domain.name

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        verbose_name = '域名截图'
        verbose_name_plural = verbose_name
