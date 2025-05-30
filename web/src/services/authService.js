import axios from 'axios';

const AUTH_API = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/auth';

/**
 * Login user with credentials
 * @param {Object} credentials - User credentials {email, password}
 * @returns {Promise<Object>} - User data and token
 */
export const login = async (credentials) => {
  // Destructure credentials
  const { email, password } = credentials;

  // Use username instead of email
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  // Post as form data
  return await axios.post(
    'http://localhost:8000/api/auth/login',
    formData,
    { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
  );
};



/**
 * Register a new user
 * @param {Object} credentials - User registration data {email, password, name}
 * @returns {Promise<Object>} - User data and token
 */
export const signup = async (credentials) => {
  try {
    // Real API call
    return await axios.post(`${AUTH_API}/signup`, credentials);
  } catch (error) {
    console.error('Signup error:', error);
    throw error;
  }
};

/**
 * Verify if a token is valid
 * @param {string} token - JWT token
 * @returns {Promise<boolean>} - Whether token is valid
 */
export const checkAuth = async (token) => {
  try {
    // Real API call
    const response = await axios.get(`${AUTH_API}/verify`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    return response.data.verified;
  } catch (error) {
    console.error('Auth verification error:', error);
    return false;
  }
};
