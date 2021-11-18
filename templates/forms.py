from django.db.models import fields
from django.forms import ModelForm
from base.models import Rooms

class roomform(ModelForm):
    class Meta:
        model = Rooms
        fields = '__all__'
