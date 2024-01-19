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

// Use Pinia for state management
// app.use(createPinia());

const piniaSocketStore = useSocketStoreWithOut(app);

app.use(VueNativeSock, "", {
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
