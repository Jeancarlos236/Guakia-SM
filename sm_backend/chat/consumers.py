# consumers.py

import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, ConversationMessage
from .serializer import ConversationMessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    def getData(self, chat_message):
        serializer=ConversationMessageSerializer(chat_message)
        return serializer.data

    async def receive(self, text_data):
        try:    
            text_data_json = json.loads(text_data)
            type = text_data_json.get("type", text_data_json)
            
            if(type == 'chat-message'):
                message = text_data_json.get("message", text_data_json)
                sent_to_user_id=text_data_json.get('sent_to')
                created_by_user_id=text_data_json.get('created_by')
                conversation_id=text_data_json.get('conversation_id')
                conversation = await sync_to_async(Conversation.objects.get)( id=conversation_id )
                
                # Save the message to the database
                chat_message=await sync_to_async(ConversationMessage.objects.create)(
                    conversation=conversation,
                    body=message,
                    sent_to_id=sent_to_user_id,
                    created_by_id=created_by_user_id,
                )
                
                data = await sync_to_async(self.getData)(chat_message=chat_message)
                
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': "chat_message",
                        "info": data
                    }
                )
        except json.JSONDecodeError:
            # Handle the case where text_data is not a valid JSON
            await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': "error",
                        "message": "Invalid JSON format"
                    }
                )
            
    async def chat_message(self, event):
        data = event['info']
        await self.send(text_data=json.dumps({"type": "chat-message","info":data}))

    # Add this method to set the channel_layer
    def set_channel_layer(self, channel_layer):
        self.channel_layer = channel_layer
