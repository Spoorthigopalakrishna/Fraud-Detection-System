import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

export const predictTransaction = async (formData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/predict`, formData);
    return response.data;
  } catch (error) {
    throw error;
  }
};
