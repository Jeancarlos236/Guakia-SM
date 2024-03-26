import json

from channels.generic.websocket import WebsocketConsumer
from .models import Conversation, ConversationMessage
from .serializer import ConversationMessageSerializer
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({"type": "connected"}))
        

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        try:    
            text_data_json = json.loads(text_data)
            type = text_data_json.get("type", text_data_json)
            
            if(type == 'chat-message'):
                message = text_data_json.get("message", text_data_json)
                sent_to_user_id=text_data_json.get('sent_to')
                created_by_user_id=text_data_json.get('created_by')
                conversation_id=text_data_json.get('conversation_id')
                conversation = Conversation.objects.get( id=conversation_id )

                # Save the message to the database
                chat_message=ConversationMessage.objects.create(
                    conversation=conversation,
                    body=message,
                    sent_to_id=sent_to_user_id,
                    created_by_id=created_by_user_id,
                )
                serializer=ConversationMessageSerializer(chat_message)
                self.send(text_data=json.dumps({"type": "chat-message","info":serializer.data}))
        except json.JSONDecodeError:
            # Handle the case where text_data is not a valid JSON
            self.send(text_data=json.dumps({"message": "Invalid JSON format"}))
