import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth'; // Importamos el store de Pinia

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
    meta: { requiresAuth: true } // Protegemos esta ruta
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

// Guardias de navegación (Navigation Guards)
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated;
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Si la ruta requiere autenticación y el usuario no está logueado,
    // lo redirigimos a la página de login
    next({ name: 'LoginPage' });
  } else if ((to.name === 'LoginPage' || to.name === 'RegisterPage') && isAuthenticated) {
    // Si el usuario está logueado y trata de ir a Login o Register,
    // lo redirigimos al perfil
    next({ name: 'UserProfilePage' });
  } else {
    // Si no hay restricciones, o si se cumplen, la navegación continúa
    next();
  }
});

export default router;
