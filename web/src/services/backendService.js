import axios from 'axios';

export const fetchRelevantDocs = async (query, token) => {
  const res = await axios.post(
    'http://localhost:8000/api/retrieve',
    { query },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return res.data.documents;
};
