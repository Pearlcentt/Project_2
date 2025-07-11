// src/services/backendService.js
// This service handles API communication with your FastAPI backend

const API_URL = 'http://localhost:8000/api';

/**
 * Fetches relevant documents from the backend based on user query
 * @param {string} query - The user's question or search query
 * @param {string} token - Authentication token (optional)
 * @returns {Promise<Array>} - Array of relevant document contents
 */
export const fetchRelevantDocs = async (query, token = null) => {
  try {
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` })
    };
    
    const response = await fetch(`${API_URL}/retrieve`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ query })
    });
    
    if (!response.ok) {
      throw new Error(`Error fetching documents: ${response.status}`);
    }
    
    const data = await response.json();
    return data.documents || [];
  } catch (error) {
    console.error('Error fetching documents:', error);
    return [];
  }
};

/**
 * Calls Gemini API via our backend to generate a response
 * @param {string} input - The formatted prompt including context and query
 * @param {string} token - Authentication token (optional)
 * @returns {Promise<string>} - Gemini's generated response
 */
export const callGemini = async (input, token = null) => {
  try {
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` })
    };
    
    const response = await fetch(`${API_URL}/gemini`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ query: input })
    });
    
    if (!response.ok) {
      throw new Error(`Error calling Gemini: ${response.status}`);
    }
    
    const data = await response.json();
    return data.output || 'Sorry, I could not generate a response.';
  } catch (error) {
    console.error('Error calling Gemini:', error);
    throw error;
  }
};

/**
 * Ask a question with RAG (Retrieval-Augmented Generation)
 * This will retrieve relevant documents and generate an answer
 * @param {string} query - The user's question
 * @param {string} token - Authentication token
 * @returns {Promise<Object>} - Response with generated answer and documents
 */
export const askWithRag = async (query, token) => {
  try {
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    };

    console.log("Token used:", token);
    
    const response = await fetch(`${API_URL}/ask`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ query })
    });
    
    if (!response.ok) {
      throw new Error(`Error with RAG: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error with RAG:', error);
    throw error;
  }
};
