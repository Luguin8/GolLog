import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // <-- Importa el router desde su archivo
import axios from 'axios';

// Configura la URL base de tu API de Django
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';

const app = createApp(App);
app.use(router); // <-- Le dice a la app que use el router importado
app.mount('#app');