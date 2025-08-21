<template>
  <div class="register-container">
    <div class="card">
      <h2 class="card-title">Registro de Usuario</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">Usuario:</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" required />
        </div>
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <div v-if="error" class="error-message">
          <p v-for="(err, field) in error" :key="field">
            {{ field }}: {{ err.join(', ') }}
          </p>
        </div>
        <button type="submit" :disabled="loading" class="btn btn-primary">
          <span v-if="loading">Cargando...</span>
          <span v-else>Registrarse</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

export default {
  name: 'RegisterPage',
  setup() {
    const username = ref('');
    const email = ref('');
    const password = ref('');
    const loading = ref(false);
    const error = ref(null);

    const router = useRouter();
    const authStore = useAuthStore();

    const handleRegister = async () => {
      loading.value = true;
      error.value = null;

      const result = await authStore.register({
        username: username.value,
        email: email.value,
        password: password.value,
      });

      if (result.success) {
        alert('Registro exitoso. ¡Ahora puedes iniciar sesión!');
        router.push('/login');
      } else {
        error.value = result.error;
      }

      loading.value = false;
    };

    return {
      username,
      email,
      password,
      loading,
      error,
      handleRegister,
    };
  },
};
</script>

<style scoped>
/* Estilos del componente de Registro */
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 50px 0;
}

.card {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: left;
}

.card-title {
  text-align: center;
  color: #368f6d;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

.error-message {
  color: #d9534f;
  background-color: #f2dede;
  border: 1px solid #ebccd1;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 15px;
  text-align: center;
}

.btn-primary {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #42b983;
  color: white;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  background-color: #368f6d;
}

.btn-primary:disabled {
  background-color: #a0a0a0;
  cursor: not-allowed;
}
</style>
