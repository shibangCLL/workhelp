from django.db import models
from django.contrib.auth.models import AbstractUser


# 扩展的用户表
class UserInfo(AbstractUser):
    """用户信息表:经理，组长，员工"""
    gender_type = (("male", "男"), ("female", "女"))
    gender = models.CharField(choices=gender_type, null=True, blank=True, max_length=12)
    mobile_phone = models.CharField(max_length=11, null=True, blank=True, unique=True)

    def __str__(self):
        return self.username
