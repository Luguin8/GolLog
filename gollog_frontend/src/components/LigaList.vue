<template>
  <div class="liga-list">
    <h1>Ligas de Fútbol</h1>
    <p v-if="loading">Cargando ligas...</p>
    <p v-if="error">{{ error }}</p>
    <ul v-if="ligas.length">
      <li v-for="liga in ligas" :key="liga.id">
        <router-link :to="{ name: 'EquiposByLiga', params: { ligaId: liga.id } }" class="liga-link">
          {{ liga.nombre }} ({{ liga.pais }})
        </router-link>
      </li>
    </ul>
    <p v-else-if="!loading && !error">No se encontraron ligas. Ejecuta 'python manage.py import_sports_data' en el backend.</p>
  </div>
</template>

<script>
import axios from 'axios'; // Importa Axios

export default {
  name: 'LigaList',
  data() {
    return {
      ligas: [],
      loading: true,
      error: null,
    };
  },
  // 'created' es un hook del ciclo de vida de Vue que se ejecuta después de que la instancia del componente ha sido creada.
  created() {
    this.fetchLigas();
  },
  methods: {
    async fetchLigas() {
      try {
        // Axios ya tiene la URL base ('http://127.0.0.1:8000/api/') configurada en main.js
        const response = await axios.get('ligas/'); 
        this.ligas = response.data;
        this.loading = false;
      } catch (error) {
        console.error("Error al cargar las ligas:", error);
        this.error = "No se pudieron cargar las ligas. Verifica que el backend esté corriendo y la API Key sea correcta.";
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Estilos básicos para el componente LigaList */
.liga-list {
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
}

li {
  background-color: #f9f9f9;
  margin-bottom: 10px;
  padding: 10px 15px;
  border-radius: 5px;
  border: 1px solid #eee;
}

.liga-link {
  text-decoration: none;
  color: #2c3e50;
  font-weight: bold;
  display: block;
  padding: 0;
}

.liga-link:hover {
  color: #42b983;
}

p {
  text-align: center;
  color: #666;
}

p.error {
  color: red;
  font-weight: bold;
}
</style>