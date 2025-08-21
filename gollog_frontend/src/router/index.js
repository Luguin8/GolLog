import { createRouter, createWebHistory } from 'vue-router';

// Importar todos los componentes de la aplicación
import HomePage from '../components/HomePage.vue';
import LigaList from '../components/LigaList.vue';
import EquiposByLiga from '../components/EquiposByLiga.vue';
import AllMatchesPage from '../components/AllMatchesPage.vue';
import EquipoDetailPage from '../components/EquipoDetailPage.vue';
import UserProfilePage from '../components/UserProfilePage.vue';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/ligas',
    name: 'LigaList',
    component: LigaList,
  },
  {
    path: '/ligas/:ligaId',
    name: 'EquiposByLiga',
    component: EquiposByLiga,
    props: true,
  },
  {
    path: '/partidos',
    name: 'AllMatchesPage',
    component: AllMatchesPage,
  },
  {
    path: '/equipos/:equipoId',
    name: 'EquipoDetailPage',
    component: EquipoDetailPage,
    props: true,
  },
  {
    path: '/perfil',
    name: 'UserProfilePage',
    component: UserProfilePage,
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: RegisterPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
