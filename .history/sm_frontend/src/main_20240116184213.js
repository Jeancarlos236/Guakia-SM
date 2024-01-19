import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import "./assets/main.css";
import { useSocketStoreWithOut } from "@/stores/socket";
import VueNativeSock from "vue-native-websocket-vue3";

const app = createApp(App);
// Set up the global axios configuration
axios.defaults.baseURL = "http://127.0.0.1:8000";

const piniaSocketStore = useSocketStoreWithOut(app);

app.use(VueNativeSock, `dsfd`, {
	// ws://127.0.0.1:8000/ws/chat/${conversationId}/
	store: piniaSocketStore,

	format: "json",
	connectManually: true,
	reconnection: true,

	reconnectionAttempts: 5,

	reconnectionDelay: 3000,
});

// Use the router and axios
app.use(router, axios);

// Mount the app to the DOM
const main = app.mount("#app");

export default main;
