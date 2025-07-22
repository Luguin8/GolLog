<template>
  <div id="app">
    <LigaList />
  </div>
</template>

<script>
import LigaList from './components/LigaList.vue'; // Importa tu nuevo componente

export default {
  name: 'App',
  components: {
    LigaList, // Declara el componente para que pueda ser usado en la plantilla
  },
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
  margin-top: 60px;
}
</style>