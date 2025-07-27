import { createRouter, createWebHistory } from 'vue-router';
import LigaList from '../components/LigaList.vue';
import EquiposByLiga from '../components/EquiposByLiga.vue'; // Asegúrate de que el nombre del componente sea este

const routes = [
  {
    path: '/',
    name: 'LigaList',
    component: LigaList,
  },
  {
    path: '/ligas/:ligaId',
    name: 'EquiposByLiga',
    component: EquiposByLiga,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;