import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios' // importa axios

// config la url base de api django
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/'

createApp(App).mount('#app')
