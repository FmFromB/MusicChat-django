from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name")

class RoomSerializers(serializers.ModelSerializer):
    creator = UserSerializer()
    invited = UserSerializer(many=True)
    class Meta:
        model = Room
        fields = ("id", "creator", "invited", "date")

class ChatSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Chat
        fields = ("user", "text", "date")

class ChatPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ("room", "text")