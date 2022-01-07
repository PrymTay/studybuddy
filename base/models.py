from django.db import models
from django.db.models.fields import DateTimeField
from django.contrib.auth.models import User
from django.http.request import MediaType

# Create your models here.

class Rooms(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic =  models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True) #'' around Topic cause topic is below and not above the room classs
    name = models.CharField(max_length=20)
    participants = models.ManyToManyField(User,related_name='participants', blank=True)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_At = DateTimeField(auto_now_add=True) #takes timestamp at creation only

    
    class Meta:
        ordering = ['-updated_at','-created_At']  #ensure that the most recent room appears at the top

    def __str__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True) #takes timestamp at creation only

    def __str__(self):
        return self.body[0:50]



     

