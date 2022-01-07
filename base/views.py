from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.models import User
from templates.forms import roomform
from .models import Rooms, Topic, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages

# Create your views here.


def home(request):
    # use the get (request method) and the get(method--models get method haha funny)
    # 'query' is the one appended in the url
    query = request.GET.get('query')  if request.GET.get('query') != None else ''
    rooms = Rooms.objects.filter(
        Q(topic__title__icontains=query)|
        Q(description__icontains=query)
         # Q(host__icontains=query)
        )  #contains - if serach has any similar character, 
           #i - for case insensitive __ - just the way we are adding it to the model search
    topics = Topic.objects.all()

    room_count = rooms.count() # getting the number of rooms returned from the search. and its faster than .len()
    context = {"rooms":rooms,"topics":topics ,"room_count":room_count }
    return render(request,'index.html',context)

def room(request, pk ):
    rooms = Rooms.objects.get(id=pk)
    room_messages = rooms.message_set.all().order_by('created_at')# this gives the children of that model... basically you just get the model name, in lower caps(so messages instead of Messages)
    
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room = rooms,
            body=request.POST.get('body')
        )
        return redirect('room',pk)
    context = {"rooms":rooms,"room_messages":room_messages}
    return render(request,'room.html', context)

@login_required(login_url='login')
def create_room(request):
    form = roomform()
    if request.method == 'POST':
        form = roomform(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
        
    context = {"form":form}
    return render(request,'room_form.html',context)

@login_required(login_url='login')
def update_room(request,pk):
    rooms = Rooms.objects.get(id=pk)
    form = roomform(instance=rooms)

    #ensuring that only the  room ownwer can edit that room
    if request.user != rooms.host:
        return HttpResponse("It's rude to edit other people's rooms!!!")

    if request.method == 'POST':
        form = roomform(request.POST, instance=rooms) #to make sure that we are updating that particular room details
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'room_form.html',context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Rooms.objects.get(id=pk)

 #ensuring that only the room ownwer can delet that room
    if request.user != room.host:
        return HttpResponse("It's rude to delete other people's rooms!!!")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'delete.html',{'object':room})  

def login_page(request):
    page = 'login'
    #stopping an already logged in user from logging in again.
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid credentials')

    context = {"page":page}
    return render(request,'login_register.html',context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  #we want to be able to access the form
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
    context = {'form':form}
    return render(request,'login_register.html',context)