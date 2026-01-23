import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = process.env.EXPO_PUBLIC_BACKEND_URL || 'https://drivingiq-test.preview.emergentagent.com';

const api = axios.create({
  baseURL: `${API_URL}/api`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth API
export const authAPI = {
  register: async (name: string, email: string, password: string) => {
    const response = await api.post('/auth/register', { name, email, password });
    return response.data;
  },
  
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },
  
  getMe: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Modules API
export const modulesAPI = {
  getModules: async () => {
    const response = await api.get('/modules');
    return response.data;
  },
  
  getModuleQuestions: async (modulo: string, limit: number = 10, skip: number = 0) => {
    const response = await api.get(`/modules/${modulo}/questions`, {
      params: { limit, skip }
    });
    return response.data;
  },
  
  getQuestionWithAnswer: async (modulo: string, questionId: string) => {
    const response = await api.get(`/modules/${modulo}/question/${questionId}`);
    return response.data;
  },
};

// Simulation API
export const simulationAPI = {
  startNew: async () => {
    const response = await api.get('/simulation/new');
    return response.data;
  },
  
  submit: async (answers: Array<{question_id: string; selected_option: string}>, time_taken_seconds: number) => {
    const response = await api.post('/simulation/submit', {
      answers,
      time_taken_seconds,
    });
    return response.data;
  },
  
  getResult: async (simulationId: string) => {
    const response = await api.get(`/simulation/${simulationId}`);
    return response.data;
  },
};

// History API
export const historyAPI = {
  getHistory: async (limit: number = 20) => {
    const response = await api.get('/history', { params: { limit } });
    return response.data;
  },
  
  getStats: async () => {
    const response = await api.get('/stats');
    return response.data;
  },
};

export default api;
