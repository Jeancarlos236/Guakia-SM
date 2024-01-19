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
// Set up the global axios configuration
axios.defaults.baseURL = "http://127.0.0.1:8000";

// Use Pinia for state management
// app.use(createPinia());

const piniaSocketStore = useSocketStoreWithOut(app);

app.use(
  VueNativeSock,
  `wss://www.kaisir.cn/websocket/${localStorage.getItem("userID")}`,
  {
    // 启用pinia集成 | enable pinia integration
    store: piniaSocketStore,
    // 数据发送/接收使用使用json
    format: "json",
    // 开启手动调用 connect() 连接服务器
    connectManually: true,
    // 开启自动重连
    reconnection: true,
    // 尝试重连的次数
    reconnectionAttempts: 5,
    // 重连间隔时间
    reconnectionDelay: 3000
  }


// Use the router and axios
app.use(router, axios);

// Mount the app to the DOM
const main = app.mount("#app");

export default main;
