from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Room, Message

# Create your views here.
def home(request):
    return render(request, "home.html")

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)

    return render(request, "room.html", {
        "room": room,
        "username": username,
        "room_details": room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect("/" + room + "/?username=" + username)

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details)

    return JsonResponse({
        "messages": list(messages.values())
    })

def send(request):
    username = request.POST['username']
    room_id = request.POST['room_id']
    message = request.POST['message']

    new_message = Message.objects.create(
        value=message,
        user=username,
        room=Room.objects.get(id=room_id)
    )

    new_message.save()

    return JsonResponse({"status": "Message sent successfully"})



def health_check(request):
    return JsonResponse({"status": "healthy"})