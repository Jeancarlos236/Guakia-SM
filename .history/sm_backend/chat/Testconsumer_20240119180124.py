import json

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print("Received text_data:", text_data)
        try:    
            text_data_json = json.loads(text_data)
            print("Parsed text_data_json:", text_data_json)
            message = text_data_json["message"]
            self.send(text_data=json.dumps({"message": message}))
        except json.JSONDecodeError:
            # Handle the case where text_data is not a valid JSON
            self.send(text_data=json.dumps({"message": "Invalid JSON format"}))
