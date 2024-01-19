// socketService.js

import { io } from "socket.io-client";

const socket = io(
	`ws://127.0.0.1:8000/ws/chat/24922c0a-929b-446a-8445-f97340f0ce95/`,
); // Replace with your Django server URL

export default socket;
