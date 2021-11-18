from django.shortcuts import render

from templates.forms import roomform
from .models import Rooms

# Create your views here.

rooms= [
    {'id':1,"name":"django"},
     {'id':2,"name":"python"},
      {'id':3,"name":"java"},
       {'id':4,"name":"C++"},
]



def home(request):
    rooms = Rooms.objects.all()
    context = {"rooms":rooms}
    return render(request,'index.html',context)

def room(request, pk ):
    rooms = Rooms.objects.get(id=pk)
    context = {"rooms":rooms}
    return render(request,'room.html', context)

def create_room(request):
    form = roomform()
    context = {"form":form}
    return render(request,'room_form.html' ,context)