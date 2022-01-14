from django.db.models import fields
from django.forms import ModelForm
from base.models import Message, Rooms

class roomform(ModelForm):
    class Meta:
        model = Rooms
        fields = '__all__'
        exclude = ['host','participants']

class messageform(ModelForm):
    class Meta:
        model = Message
        fields = ['body']