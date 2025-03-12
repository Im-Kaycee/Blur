from django.urls import path
from chat.views import *

urlpatterns = [
    path('', home1, name='index'),
    path('chat', chat_view, name='home'),
    path('chat/new_groupchat/', create_groupchat, name='new-groupchat'),
    path('chat/edit/<chatroom_name>', chatroom_edit_view, name='edit-chatroom'),
    path('chat/delete/<chatroom_name>', chatroom_delete_view, name="chatroom-delete"),
    path('chat/leave/<chatroom_name>', chatroom_leave_view, name="chatroom-leave"),
    path('chat/<str:username>/', get_or_create_chatroom, name='start-chat'),
    path('chat/room/<str:chatroom_name>/', chat_view, name='chatroom'),
    
]

