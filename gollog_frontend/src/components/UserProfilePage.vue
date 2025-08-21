<template>
  <div class="profile-container">
    <div class="card">
      <h2 class="card-title">Hola, {{ authStore.user.username }}</h2>
      <p>¡Bienvenido a tu perfil!</p>
      <p>Desde aquí podrás gestionar tus datos y ver tu historial de partidos.</p>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth';

export default {
  name: 'UserProfilePage',
  setup() {
    const authStore = useAuthStore();
    return {
      authStore,
    };
  },
};
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 50px 0;
  text-align: center;
}

.card {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

.card-title {
  color: #368f6d;
  margin-bottom: 10px;
}
</style>
