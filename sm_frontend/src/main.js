import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import VueNativeSock from "vue-native-websocket";

const app = createApp(App);

// Use the WebSocket plugin
app.use(VueNativeSock, "ws://" + window.location.host + "/ws/chat/");

// Set up the global axios configuration
axios.defaults.baseURL = "http://127.0.0.1:8000";

// Use Pinia for state management
app.use(createPinia());

// Use the router and axios
app.use(router);
app.use(axios);

// Mount the app to the DOM
app.mount("#app");
