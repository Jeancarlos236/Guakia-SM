import json

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({"type": "connected"}))
        

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print("Received text_data:", text_data)
        try:    
            text_data_json = json.loads(text_data)
            #print("Parsed text_data_json:", text_data_json)
            message = text_data_json.get("type", text_data_json)
            
            if(type == 'chat-message'):
                message = text_data_json.get("message", text_data_json)
                self.send(text_data=json.dumps({"message": message}))
        except json.JSONDecodeError:
            # Handle the case where text_data is not a valid JSON
            self.send(text_data=json.dumps({"message": "Invalid JSON format"}))
