
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.models import User
from django.template import context
from django.urls import reverse_lazy
from templates.forms import messageform, roomform
from .models import Rooms, Topic, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages

# Create your views here.

def topic_count(request):
     query = request.GET.get('query') if request.GET.get(
        'query') != None else ''
     topics = Topic.objects.filter(Q(title__icontains=query))
     topic_count = topics.count()
      
     context = {"topic_count":topic_count}
     print(context)
     return render(request,'topic-component.html',context)

def home(request):
    # use the get (request method) and the get(method--models get method haha funny)
    # 'query' is the one appended in the url
    query = request.GET.get('query') if request.GET.get(
        'query') != None else ''
    therooms = Rooms.objects.all()
    rooms = Rooms.objects.filter(
        Q(topic__title__icontains=query) |
        Q(description__icontains=query)
        # Q(host__icontains=query)
    )  # contains - if serach has any similar character,
    # i - for case insensitive __ - just the way we are adding it to the model search
    topics = Topic.objects.all()
    # topicsperroom = therooms.rooms_set.all()
    # print(topicsperroom)
    # count = topicsperroom.count()


    topics = Topic.objects.filter(Q(title__icontains=query))
    room_count = topics.count()
    # getting the number of rooms returned from the search. and its faster than .len()
    #room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__title__icontains=query))[0:5] #limiting the number of object returned and adding a filter 
    context = {"rooms": rooms, "topics": topics, "room_count": room_count,"room_messages":room_messages}
    return render(request, 'index.html', context)

def userProfile(request,pk):
    userObj = User.objects.get(id=pk)
    rooms = userObj.rooms_set.all() #getting the rooms a user is subscribed too
    room_messages = userObj.message_set.all()[0:5] #getting any mesages that user has sent ps:_set.all()this aplies for children
    room_count = rooms.count()
    topics = Topic.objects.all()
    
    context = {"userObj":userObj, "rooms":rooms, 
               "room_messages":room_messages,
               "room_count":room_count,"topics": topics}
    print(context) 
    return render(request,'profile.html',context)

def room(request, pk):
    rooms = Rooms.objects.get(id=pk)
    # this gives the children of that model... basically you just get the model name, in lower caps(so messages instead of Messages)
    room_messages = rooms.message_set.all().order_by('created_at')
    participants = rooms.participants.all()
    p_count = participants.count()
   
    if request.method == 'POST':
       
        message = Message.objects.create(
            user=request.user,
            room=rooms,
            body=request.POST.get('body')
        )

        rooms.participants.add(request.user)
        return redirect('room', pk=rooms.id)
    context = {"rooms": rooms, "room_messages": room_messages,
               "participants": participants,'p_count':p_count}
    return render(request, 'room.html', context)


@login_required(login_url='login')
def create_room(request):
    form = roomform()
    if request.method == 'POST':
        form = roomform(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()

            return redirect('home')

    context = {"form": form}
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    rooms = Rooms.objects.get(id=pk)
    form = roomform(instance=rooms)

    # ensuring that only the  room ownwer can edit that room
    if request.user != rooms.host:
        return HttpResponse("It's rude to edit other people's rooms!!!")

    if request.method == 'POST':
        # to make sure that we are updating that particular room details
        form = roomform(request.POST, instance=rooms)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'room_form.html', context)

@login_required(login_url='login')
def edit_message(request, pk):
    message = Message.objects.get(id=pk)
   
    form = messageform(instance=message)
    

    # ensuring that only the  room ownwer can edit that room
    if request.user != message.user:
        return HttpResponse("It's rude to edit other people's messages!!!")

    if request.method == 'POST':
        
        # to make sure that we are updating that particular message's details
        form = messageform(request.POST, instance=message)
        if form.is_valid:
            
            form.save()
            # return HttpResponseRedirect(request.session['form'])
            # next = request.POST.get('next', '/')
            # return HttpResponseRedirect(next)
            return redirect('home')
    context = {'form': form}
    return render(request, 'room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Rooms.objects.get(id=pk)

 # ensuring that only the room ownwer can delete that room
    if request.user != room.host:
        return HttpResponse("It's rude to delete other people's rooms!!!")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'object': room})


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

 # ensuring that only the message ownwer can delete that message
    if request.user != message.user:
        return HttpResponse("It's rude to delete other people's messages!!!")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'delete.html', {'object': message})


def login_page(request):
    #page = 'login'
    # stopping an already logged in user from logging in again.
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')

    #context = {"page": page}
    return render(request,'login_register.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = UserCreationForm
    success_url = reverse_lazy('login')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # we want to be able to access the form
            user = form.save(commit=False)
            user.firstname = user.firstname.lower()
            user.lastname = user.lastname.lower()
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    else:
        messages.error(request, 'Not a post request')
    context = {'form': form}
    return render(request, 'signup.html', context)

