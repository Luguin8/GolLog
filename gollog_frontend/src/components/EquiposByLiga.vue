<template>
  <div class="equipos-liga">
    <h1>Equipos de la Liga</h1>
    <p v-if="loading">Cargando equipos...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <ul v-if="equipos.length">
      <li v-for="equipo in equipos" :key="equipo.id">
        <img :src="equipo.logo_imagen || equipo.logo_url" :alt="equipo.nombre" class="logo">
        <h3>{{ equipo.nombre }}</h3>
      </li>
    </ul>
    <p v-else-if="!loading && !error">No se encontraron equipos para esta liga.</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EquiposByLiga',
  props: ['ligaId'], // Recibe el ID de la liga como una prop
  data() {
    return {
      equipos: [],
      loading: true,
      error: null,
    };
  },
  watch: {
    // Observa cambios en el prop ligaId para recargar los equipos si la ruta cambia
    ligaId: 'fetchEquipos',
  },
  created() {
    this.fetchEquipos();
  },
  methods: {
    async fetchEquipos() {
      this.loading = true;
      this.error = null;
      try {
        // Usa el ID de la liga para filtrar los equipos
        const response = await axios.get(`equipos/?liga=${this.ligaId}`);
        this.equipos = response.data.results;
      } catch (error) {
        console.error("Error al cargar los equipos:", error);
        this.error = "No se pudieron cargar los equipos.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.equipos-liga {
  max-width: 800px;
  margin: 50px auto;
}
.logo {
  width: 50px;
  height: 50px;
  margin-right: 15px;
}
li {
  display: flex;
  align-items: center;
  justify-content: center;
}
.error {
  color: red;
  font-weight: bold;
}
</style>