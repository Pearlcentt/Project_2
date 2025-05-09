import axios from 'axios';

const API = process.env.REACT_APP_GEMINI_API_URL || 'http://localhost:8000/api/gemini';

export const callGemini = async (input, token = null) => {
  try {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    
    const res = await axios.post(
      API,
      { query: input },
      { headers }
    );
    return res.data.output;
  } catch (error) {
    console.error('Error calling Gemini:', error);
    throw error;
  }
};