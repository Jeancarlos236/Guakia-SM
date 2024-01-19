import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import "./assets/main.css";
import { useSocketStoreWithOut } from "@/store/pinia/useSocketStore";
import VueNativeSock from "vue-native-websocket-vue3";
import { setupStore } from "./stores/store";
const app = createApp(App);
const piniaSocketStore = useSocketStoreWithOut(app);
// Set up the global axios configuration
axios.defaults.baseURL = "http://127.0.0.1:8000";

// Use Pinia for state management
// app.use(createPinia());

setupStore(app);

// Use the router and axios
app.use(router, axios);

// Mount the app to the DOM
const main = app.mount("#app");

export default main;
