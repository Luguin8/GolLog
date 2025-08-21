<template>
  <div class="login-container">
    <div class="card">
      <h2 class="card-title">Iniciar Sesión</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Usuario:</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        <button type="submit" :disabled="loading" class="btn btn-primary">
          <span v-if="loading">Cargando...</span>
          <span v-else>Iniciar Sesión</span>
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
  name: 'LoginPage',
  setup() {
    const username = ref('');
    const password = ref('');
    const loading = ref(false);
    const error = ref(null);
    
    const router = useRouter();
    const authStore = useAuthStore();

    const handleLogin = async () => {
      loading.value = true;
      error.value = null;
      
      const result = await authStore.login(username.value, password.value);
      
      if (result.success) {
        router.push('/perfil');
      } else {
        error.value = result.error;
      }
      
      loading.value = false;
    };

    return {
      username,
      password,
      loading,
      error,
      handleLogin,
    };
  },
};
</script>

<style scoped>
.login-container {
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
