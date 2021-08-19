# Create your models here.
from django.db import models
from django_undeletable.models import BaseModel


class EmailLog(BaseModel):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=250)
    message = models.TextField()

    class Meta(BaseModel.Meta):
        verbose_name = 'SpamLog'
        verbose_name_plural = 'SpamLogs'
