from django.shortcuts import render
from django.db.models import Q
from rest_framework.response import Response 
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import (RoomSerializers, ChatSerializer, ChatPostSerializer, UserSerializer)
from .models import *

class RoomView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        rooms = Room.objects.filter(Q(creator=request.user) | Q(invited=request.user))
        serializer = RoomSerializers(rooms, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        Room.objects.create(creator=request.user)
        return Response(status=201)

class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        room = request.GET.get("room")
        chat = Chat.objects.filter(room=room)
        chat = Chat.objects.order_by('-id')
        serializer = ChatSerializer(chat, many=True)
        return Chat.objects.all()

    def post(self, request):
        if request.method == 'POST':
            chat = ChatPostSerializer(data=request.data)
            if chat.is_valid():
                chat.save(user=request.user)
                return Response(chat.data, status=201)
            else:
                return Response(chat.errors, status=400)
        return Response(data)


class AddUserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
     
    def post(self, request):
        room = request.data.get("room")
        user = request.data.get("user")
        try:
            room = Room.objects.get(id=room)
            room.invited.add(user)
            room.save()
            return Response(status=201)
        except:
            return Response(status=400)
