from django.shortcuts import render, HttpResponse
from .models import Room

# Create your views here.

def index(request, user_name):
    return render(request, './room/index.html',{
        'rooms' : Room.objects.all(),
        'user_name' : user_name,
    })

def room_view(request, room_name, user_name):
    chat_room, created = Room.objects.get_or_create(Rname=room_name)
    return render(request, './room/chat_view.html', {
        'room': chat_room,
        'user_name' : user_name,
    })

def logout():
    return HttpResponse('Log out')
