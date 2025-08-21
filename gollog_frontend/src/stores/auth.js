import { defineStore } from 'pinia';
import axios from 'axios';

// La URL base ahora apunta directamente al puerto
const BASE_URL = 'http://127.0.0.1:8000/';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    isAuthenticated: false,
  }),
  persist: true,

  actions: {
    async login(username, password) {
      try {
        // La URL de login no necesita el prefijo 'api/'
        const res = await axios.post(`${BASE_URL}api-token-auth/`, { username, password });
        
        this.token = res.data.token;
        this.isAuthenticated = true;
        this.user = { username }; 

        return { success: true };
      } catch (error) {
        this.token = null;
        this.user = null;
        this.isAuthenticated = false;
        
        if (error.response && error.response.data && error.response.data.non_field_errors) {
          return { success: false, error: error.response.data.non_field_errors[0] };
        } else if (error.response && error.response.data && error.response.data.detail) {
          return { success: false, error: error.response.data.detail };
        } else {
          return { success: false, error: 'Ocurrió un error inesperado. Por favor, intenta de nuevo.' };
        }
      }
    },

    async register(userData) {
      try {
        // La URL de registro sí necesita el prefijo 'api/'
        await axios.post(`${BASE_URL}api/register/`, userData);
        return { success: true };
      } catch (error) {
        return { success: false, error: error.response.data };
      }
    },

    logout() {
      this.token = null;
      this.user = null;
      this.isAuthenticated = false;
    },
  },
});
