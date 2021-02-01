from django.urls import path
from .views import *

urlpatterns = [
	path('room/', RoomView.as_view()),
	path('chat/', ChatView.as_view()),
	path('users/', AddUserView.as_view())
]