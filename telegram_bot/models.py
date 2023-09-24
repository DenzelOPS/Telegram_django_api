from django.db import models
from django.contrib.auth.models import User

class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    message = models.CharField(max_length=1000)
    time = models.IntegerField()    

class TelegramData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_token = models.CharField(max_length=100)
    telegram_chat_id = models.CharField(max_length=100)
