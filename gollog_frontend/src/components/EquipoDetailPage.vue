<template>
  <div class="equipo-detail-page">
    <h2>Detalles del Equipo</h2>
    <p>Aquí se mostrará la información detallada de un equipo, incluyendo sus partidos.</p>
  </div>
</template>

<script>
export default {
  name: 'EquipoDetailPage',
  props: ['equipoId'],
};
</script>

<style scoped>
.equipo-detail-page {
  padding: 20px;
}
</style>
