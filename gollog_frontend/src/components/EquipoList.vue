<template>
  <div class="equipo-list">
    <h1>Equipos de {{ ligaNombre }}</h1>
    <p v-if="loading">Cargando equipos...</p>
    <p v-if="error">{{ error }}</p>
    <ul v-if="equipos.length">
      <li v-for="equipo in equipos" :key="equipo.id" class="equipo-item">
        <img v-if="equipo.logo_url" :src="equipo.logo_url" :alt="equipo.nombre" class="equipo-logo">
        <span class="equipo-nombre">{{ equipo.nombre }}</span>
      </li>
    </ul>
    <p v-else-if="!loading && !error">No se encontraron equipos para esta liga.</p>
    <router-link to="/" class="back-link">Volver a Ligas</router-link>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EquipoList',
  props: {
    ligaId: { // Este prop DEBE coincidir con :ligaId en la ruta de main.js
      type: String,
      required: true,
    },
  },
  data() {
    return {
      equipos: [],
      ligaNombre: 'la Liga',
      loading: true,
      error: null,
    };
  },
  // Este 'watch' es crucial para cuando navegamos entre ligas sin recargar la página completa
  watch: {
    ligaId: 'fetchEquipos', // Llama a fetchEquipos cada vez que ligaId cambia
  },
  created() { // Este 'created' asegura que se carga la primera vez que se accede al componente
    this.fetchEquipos();
  },
  methods: {
    async fetchEquipos() {
      this.loading = true;
      this.error = null;
      this.equipos = []; // Limpiar equipos anteriores para evitar duplicados/datos viejos

      try {
        // Primero, obtener el nombre de la liga (opcional, pero mejora la UI)
        const ligaResponse = await axios.get(`ligas/${this.ligaId}/`);
        this.ligaNombre = ligaResponse.data.nombre || 'Desconocida';

        // Luego, obtener los equipos
        const equiposResponse = await axios.get(`equipos/?liga_id=${this.ligaId}`);
        this.equipos = equiposResponse.data;
        this.loading = false;
      } catch (error) {
        console.error("Error al cargar equipos:", error); // Esto debería aparecer en la consola
        this.error = "No se pudieron cargar los equipos. Intenta de nuevo más tarde.";
        this.loading = false;
        this.ligaNombre = 'la Liga';
      }
    },
  },
};
</script>

<style scoped>
.equipo-list {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

h1 {
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

ul {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 15px;
  justify-content: center;
}

.equipo-item {
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #eee;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.equipo-logo {
  width: 80px;
  height: 80px;
  object-fit: contain;
  margin-bottom: 10px;
}

.equipo-nombre {
  font-weight: bold;
  color: #555;
}

p {
  text-align: center;
  color: #666;
}

p.error {
  color: red;
}

.back-link {
    display: inline-block;
    margin-top: 30px;
    padding: 10px 15px;
    background-color: #007bff;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}

.back-link:hover {
    background-color: #0056b3;
}
</style>