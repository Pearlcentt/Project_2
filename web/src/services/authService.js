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


// import axios from 'axios';

// const AUTH_API = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/auth';

// /**
//  * Login user with credentials
//  * @param {Object} credentials - User credentials {email, password}
//  * @returns {Promise<Object>} - User data and token
//  */
// export const login = async (credentials) => {
//   try {
//     // For development/testing with mocked backend
//     if (process.env.REACT_APP_MOCK_AUTH === 'true') {
//       console.log('Using mock authentication');
//       return {
//         data: {
//           token: 'mock-token-for-testing',
//           user: { email: credentials.email }
//         }
//       };
//     }
    
//     // Real API call
//     return await axios.post(`${AUTH_API}/login`, credentials);
//   } catch (error) {
//     console.error('Login error:', error);
//     throw error;
//   }
// };

// /**
//  * Register a new user
//  * @param {Object} credentials - User registration data {email, password, name}
//  * @returns {Promise<Object>} - User data and token
//  */
// export const signup = async (credentials) => {
//   try {
//     // For development/testing with mocked backend
//     if (process.env.REACT_APP_MOCK_AUTH === 'true') {
//       console.log('Using mock authentication');
//       return {
//         data: {
//           token: 'mock-token-for-testing',
//           user: { email: credentials.email, name: credentials.name }
//         }
//       };
//     }
    
//     // Real API call
//     return await axios.post(`${AUTH_API}/signup`, credentials);
//   } catch (error) {
//     console.error('Signup error:', error);
//     throw error;
//   }
// };

// /**
//  * Verify if a token is valid
//  * @param {string} token - JWT token
//  * @returns {Promise<boolean>} - Whether token is valid
//  */
// export const checkAuth = async (token) => {
//   try {
//     // For development/testing with mocked backend
//     if (process.env.REACT_APP_MOCK_AUTH === 'true') {
//       console.log('Using mock authentication');
//       return true;
//     }
    
//     // Real API call
//     const response = await axios.get(`${AUTH_API}/verify`, {
//       headers: { Authorization: `Bearer ${token}` }
//     });
    
//     return response.data.verified;
//   } catch (error) {
//     console.error('Auth verification error:', error);
//     return false;
//   }
// };

// // src/services/backendService.js
// /**
//  * Services for interacting with the FastAPI backend
//  */

// const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// /**
//  * Fetches relevant documents from the backend based on user query
//  * @param {string} query - The user's question or search query
//  * @param {string} token - Authentication token
//  * @returns {Promise<Array>} - Array of relevant document contents
//  */
// export const fetchRelevantDocs = async (query, token) => {
//   try {
//     const headers = {
//       'Content-Type': 'application/json',
//       'Authorization': `Bearer ${token}`
//     };
    
//     const response = await fetch(`${API_URL}/retrieve`, {
//       method: 'POST',
//       headers,
//       body: JSON.stringify({ query })
//     });
    
//     if (!response.ok) {
//       throw new Error(`Error fetching documents: ${response.status}`);
//     }
    
//     const data = await response.json();
//     return data.documents || [];
//   } catch (error) {
//     console.error('Error fetching documents:', error);
//     return [];
//   }
// };

// /**
//  * Calls Gemini API via our backend to generate a response
//  * @param {string} query - The user query to process
//  * @param {string} token - Authentication token
//  * @returns {Promise<string>} - Gemini's generated response
//  */
// export const callGemini = async (query, token) => {
//   try {
//     const headers = {
//       'Content-Type': 'application/json',
//       'Authorization': `Bearer ${token}`
//     };
    
//     const response = await fetch(`${API_URL}/gemini`, {
//       method: 'POST',
//       headers,
//       body: JSON.stringify({ query })
//     });
    
//     if (!response.ok) {
//       throw new Error(`Error calling Gemini: ${response.status}`);
//     }
    
//     const data = await response.json();
//     return data.output || 'Sorry, I could not generate a response.';
//   } catch (error) {
//     console.error('Error calling Gemini:', error);
//     throw error;
//   }
// };

// /**
//  * Ask a question with RAG (Retrieval-Augmented Generation)
//  * This will retrieve relevant documents and generate an answer
//  * @param {string} query - The user's question
//  * @param {string} token - Authentication token
//  * @returns {Promise<Object>} - Response with generated answer and documents
//  */
// export const askWithRag = async (query, token) => {
//   try {
//     const headers = {
//       'Content-Type': 'application/json',
//       'Authorization': `Bearer ${token}`
//     };
    
//     const response = await fetch(`${API_URL}/ask`, {
//       method: 'POST',
//       headers,
//       body: JSON.stringify({ query })
//     });
    
//     if (!response.ok) {
//       throw new Error(`Error with RAG: ${response.status}`);
//     }
    
//     const data = await response.json();
//     return data;
//   } catch (error) {
//     console.error('Error with RAG:', error);
//     throw error;
//   }
// };