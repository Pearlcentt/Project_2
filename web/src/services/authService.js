import axios from 'axios';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/auth';

export const login = async (credentials) => {
  console.log('Login called with:', credentials);
  return { 
    data: { 
      token: 'mock-token-for-testing',
      user: { email: credentials.email }
    } 
  };
  
  // When auth in backend:
  // return await axios.post(`${API}/login`, credentials);
};

export const signup = async (credentials) => {
  console.log('Signup called with:', credentials);
  return { 
    data: { 
      token: 'mock-token-for-testing',
      user: { email: credentials.email }
    } 
  };
  
  // When auth in backend:
  // return await axios.post(`${API}/signup`, credentials);
};

export const checkAuth = async (token) => {
  return true;
  
  // When auth in backend:
  // return await axios.get(`${API}/verify`, {
  //   headers: { Authorization: `Bearer ${token}` }
  // });
};