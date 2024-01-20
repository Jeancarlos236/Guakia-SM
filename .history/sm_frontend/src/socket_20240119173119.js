const socket = new WebSocket(`ws://localhost:8000/ws/chat/{conversationID}`);

export default socket;
