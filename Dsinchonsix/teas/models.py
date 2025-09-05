from django.db import models

# Create your models here.
from django.db import models

class TeaCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10, null=False, verbose_name="카테고리 이름")
    mood = models.CharField(max_length=20, null=False, verbose_name="기분 이름")

    def __str__(self):
        return self.name

class Tea(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10, null=False, verbose_name="차 이름")
    description = models.TextField(null=False, verbose_name="차 설명")
    tea_category = models.ForeignKey(TeaCategory, on_delete=models.CASCADE, null=False, verbose_name="카테고리 종류")
    taste = models.CharField(max_length=30, null=False, verbose_name="차 맛")

    def __str__(self):
        return self.name