
import axios from 'axios';

const API_URL = 'https://vdy14zq4rk.execute-api.eu-central-1.amazonaws.com/dev';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false
});

export const generateProductSummary = async (id: string) => {
  try {
    const response = await api.post('/invoke', {
      id,
    });

    return response.data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

export const generateFinalSummary = async (category: string, summaries: string[]) => {
  try {
    const response = await api.post('/invoke', {
      category,
      summaries,
    });

    return response.data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

export default api; 