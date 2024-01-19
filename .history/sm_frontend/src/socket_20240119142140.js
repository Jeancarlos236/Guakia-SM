import { io } from "socket.io-client";

// Example client-side code
const socket = io(`ws://localhost:8000/ws/chat/{conversationID}/`);

export default socket;
