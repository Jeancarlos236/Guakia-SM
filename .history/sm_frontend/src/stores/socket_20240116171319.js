import { defineStore } from "pinia";
import main from "/@/main";
export const useSocketStore = defineStore({
	id: "socket",
	state: () => ({
		isConnected: false,
		message: "",
		reconnectError: false,
		heartBeatInterval: 50000,
		heartBeatTimer: 0,
	}),
	actions: {
		SOCKET_ONOPEN(event) {
			this.socket = event.currentTarget;
			this.isConnected = true;

			this.heartBeatTimer = window.setInterval(() => {
				const message = "Heartbeat message";
				this.isConnected &&
					this.socket.sendObj({
						code: 200,
						msg: message,
					});
			}, this.heartBeatInterval);
		},
		SOCKET_ONCLOSE(event) {
			this.isConnected = false;
			window.clearInterval(this.heartBeatTimer);
			this.heartBeatTimer = 0;
			console.log("The line is disconnected:", new Date());
			console.log("Close event:", event);
		},
		SOCKET_ONERROR(event) {
			console.error(event);
		},
		SOCKET_ONMESSAGE(message) {
			this.message = message;
		},
		SOCKET_RECONNECT(count) {
			console.info("Message system reconnecting...", count);
			this.reconnectError = false;
		},
		SOCKET_RECONNECT_ERROR() {
			this.reconnectError = true;
		},
	},
});

export function useSocketStoreWithOut() {
	const store = useSocketStore();
	return store;
}
