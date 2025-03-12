from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from chat.models import *
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name = self.chatroom_name)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name,
        )
        self.accept()
    def disconnect(self, close_code):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name,
        )
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        
        # Create message in DB
        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom,
        )

        # Send event to the WebSocket group (don't send directly to sender)
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            self.chatroom_name, event
        )

        
    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id = message_id)
        context = {
            'message': message,
            'user':self.user,
        }
        html = render_to_string('chat/partials/chat_message_p.html', context=context)
        self.send(text_data = html)
