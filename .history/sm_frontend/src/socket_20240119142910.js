import { io } from "socket.io-client";

// Example client-side code
const socket = io(
	`ws://jeff:8000/ws/chat/24922c0a-929b-446a-8445-f97340f0ce95/`,
);

export default socket;
