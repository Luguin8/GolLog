import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios' // importa axios
import { createRouter, createWebHistory } from 'vue-router';

// importa componentes de vista
import LigaList from './components/LigaList.vue';
import EquipoList from './components/EquipoList.vue';

// config la url base de api django
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/'

//Define tus rutas 
const routes = [
    {path: '/', name:'Ligas', component: LigaList},
    // Nueva ruta para listar equipos de una liga
    { path: '/ligas/:ligaId/equipos', name: 'EquiposByLiga', component: EquipoList, props: true },
]

// Crea instancia router
const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Crea la aplicación Vue y usa el router
const app = createApp(App);
app.use(router);
app.mount('#app');