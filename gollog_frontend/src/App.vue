<template>
  <div id="app">
    <nav class="main-nav">
      <router-link to="/">Inicio (Ligas)</router-link>
      </nav>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
  // Ya no necesitas importar LigaList aquí directamente si usas router-view
  // ni declararlo en components, porque Vue Router lo manejará.
};
</script>

<style>
/* Estilos globales para la aplicación */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px; /* Reducido para dejar espacio a la navegación */
}

.main-nav {
  background-color: #42b983; /* Color de Vue */
  padding: 10px 0;
  margin-bottom: 30px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.main-nav a {
  color: white;
  text-decoration: none;
  padding: 10px 20px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.main-nav a:hover,
.main-nav a.router-link-active { /* Clase que Vue Router añade al enlace activo */
  background-color: #368f6d;
  border-radius: 5px;
}
</style>