import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';
if(!API_BASE_URL){
  console.error('VITE_API_URL is not defined in environment variables');
  throw new Error('VITE_API_URL is not defined in environment variables');
}
console.log('<--------------- API Base URL: -------------->', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;