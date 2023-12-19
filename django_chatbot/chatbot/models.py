from django.db import models
from django.utils import timezone

# Create your models here.
class Users(models.Model):
    phone = models.CharField(max_length=15)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=60)
    physical_address = models.CharField(max_length=60)


class Chats(models.Model):
    summary = models.TextField()
    user_id = models.ForeignKey(Users , on_delete= models.CASCADE)
    active = models.BooleanField(default=False)

class Logs(models.Model):
    message = models.TextField()
    response = models.TextField()
    time = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(Users , on_delete= models.CASCADE)
    chat_id = models.ForeignKey(Chats , on_delete= models.CASCADE)

