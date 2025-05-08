import axios from 'axios';

export const callGemini = async (input, token) => {
  const res = await axios.post(
    'https://api.gemini.google.com/generate',
    { input },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return res.data.output;
};
