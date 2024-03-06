import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import "./assets/main.css";
const app = createApp(App);
// Set up the global axios configuration
// axios.defaults.baseURL = "https://jean-social-media.onrender.com";
axios.defaults.baseURL = "http://127.0.0.1:8000";

// Use Pinia for state management
app.use(createPinia());

// Use the router and axios
app.use(router, axios);

// Mount the app to the DOM
const main = app.mount("#app");

export default main;
