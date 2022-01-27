
from django.db import models
from django.db.models.fields import DateTimeField
from django.contrib.auth.models import User
from django.http.request import MediaType
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# from base import admin






class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
    avatar =  models.ImageField(default='default.jpg', upload_to='images/profile_images')
    bio = models.TextField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = PhoneNumberField(null=False, blank=False, unique=True,validators=[phone_regex], max_length=17,)

    def __str__(self):
     return self.user.username




      
class Rooms(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic =  models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True) #'' around Topic cause topic is below and not above the room classs
    name = models.CharField(max_length=20)
    participants = models.ManyToManyField(User,related_name='participants', blank=True)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True) #takes timestamp at creation only

    
    class Meta:
        ordering = ['-updated_at','-created_at']  #ensure that the most recent room appears at the top

    def __str__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    body = models.TextField( )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True) #takes timestamp at creation only


    class Meta:
        ordering = ['-updated_at','-created_at']  #ensure that the most recent message appears at the top

    def __str__(self):
        return self.body[0:50] #converts an object into a string



     

