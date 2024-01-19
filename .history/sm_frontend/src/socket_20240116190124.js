// socketService.js

import { io } from "socket.io-client";

const socket = io("ws://localhost:8000/ws/chat/some_room/"); // Replace with your Django server URL

export default socket;
