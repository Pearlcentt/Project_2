import axios from 'axios';

const API = 'http://localhost:8000/api/auth'; // adjust to your backend

export const login = async (credentials) =>
  await axios.post(`${API}/login`, credentials);

export const signup = async (credentials) =>
  await axios.post(`${API}/signup`, credentials);
