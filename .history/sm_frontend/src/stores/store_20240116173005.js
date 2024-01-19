import { createPinia } from "pinia";
import { App } from "vue";

const store = createPinia();

export function setupStore(app) {
	app.use(store);
}

export { store };
