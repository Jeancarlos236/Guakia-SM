import { io } from "socket.io-client";

// Example client-side code
const socket = io(`ws://127.0.0.1:8000/ws/chat/{conversationID}/`);

export default socket;
