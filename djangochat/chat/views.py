
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from urllib.parse import quote

from .models import Room, Message


def favicon(request):
    return HttpResponse(status=204)


def home(request):
    return render(request, "home.html")


def room(request, room):
    username = request.GET.get("username", "")
    room_details = Room.objects.get(name=room)

    return render(request, "room.html", {
        "room": room,
        "username": username,
        "room_details": room_details
    })


@require_POST
def checkview(request):
    room_name = request.POST.get("room_name", "").strip()
    username = request.POST.get("username", "").strip()

    if not room_name or not username:
        return JsonResponse({
            "error": "Room name and username are required"
        }, status=400)

    Room.objects.get_or_create(name=room_name)

    return redirect(
        f"/{quote(room_name, safe='')}/?username={quote(username, safe='')}"
    )


def getMessages(request, room):
    messages = Message.objects.filter(
        room=room
    ).order_by("date")

    return JsonResponse({
        "messages": list(messages.values(
            "id", "value", "date", "user", "room"
        ))
    })


@require_POST
def send(request):
    username = request.POST.get("username", "").strip()
    room_id = request.POST.get("room_id", "").strip()
    message = request.POST.get("message", "").strip()

    if not username or not room_id or not message:
        return JsonResponse({
            "error": "Username, room ID and message are required"
        }, status=400)

    try:
        room_obj = Room.objects.get(id=room_id)
    except (Room.DoesNotExist, ValueError):
        return JsonResponse({
            "error": "Room not found"
        }, status=404)

    new_message = Message.objects.create(
        value=message,
        user=username,
        room=room_obj.name
    )

    return JsonResponse({
        "status": "Message sent successfully",
        "message_id": new_message.id
    })


def health_check(request):
    return JsonResponse({
        "status": "healthy"
    })
