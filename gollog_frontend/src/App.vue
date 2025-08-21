<template>
  <div id="app">
    <header class="app-header">
      <h1>GolLog</h1>
    </header>
    <nav class="main-nav">
      <!-- Navegación principal, usando router-link para las rutas definidas -->
      <router-link to="/">Inicio</router-link>
      <router-link to="/partidos">Todos los Partidos</router-link>
      <router-link to="/ligas">Ligas</router-link>
      <router-link to="/perfil">Mi Perfil</router-link>

      <!-- Botones de login/logout, condicionales -->
      <router-link v-if="!authStore.isAuthenticated" to="/login">Login</router-link>
      <router-link v-if="!authStore.isAuthenticated" to="/register">Registro</router-link>
      <a v-if="authStore.isAuthenticated" @click="logout" href="#">Logout</a>
    </nav>
    <main class="app-main">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import { useAuthStore } from './stores/auth'; // Importa el store de Pinia
import { useRouter } from 'vue-router'; // Importa el router

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const logout = () => {
      authStore.logout();
      router.push('/login'); // Redirige al login después de cerrar sesión
    };

    return {
      authStore,
      logout,
    };
  },
};
</script>

<style>
/* Estilos globales para la aplicación */
body {
  margin: 0;
  background-color: #f4f4f4;
  font-family: 'Inter', Arial, sans-serif;
  color: #333;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

.app-header {
  background-color: #42b983;
  color: white;
  padding: 20px 0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.app-header h1 {
  margin: 0;
  font-size: 2.5em;
}

.main-nav {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 15px 0;
  background-color: #368f6d;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.main-nav a {
  color: white;
  text-decoration: none;
  padding: 8px 15px;
  border-radius: 5px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.main-nav a:hover,
.main-nav a.router-link-active {
  background-color: #2c3e50;
}

.app-main {
  padding: 20px;
}
</style>
