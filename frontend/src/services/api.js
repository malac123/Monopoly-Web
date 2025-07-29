import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Game Management
export const createGame = async (playerName = "You") => {
  const response = await axios.post(`${API}/games`, { playerName });
  return response.data;
};

export const getGame = async (gameId) => {
  const response = await axios.get(`${API}/games/${gameId}`);
  return response.data;
};

export const getProperties = async () => {
  const response = await axios.get(`${API}/properties`);
  return response.data;
};

// Player Actions
export const rollDice = async (gameId) => {
  const response = await axios.post(`${API}/games/${gameId}/roll-dice`);
  return response.data;
};

export const handlePropertyAction = async (gameId, action, playerId, propertyId) => {
  const response = await axios.post(`${API}/games/${gameId}/property-action`, {
    action,
    playerId,
    propertyId
  });
  return response.data;
};

export const endTurn = async (gameId) => {
  const response = await axios.post(`${API}/games/${gameId}/end-turn`);
  return response.data;
};

export const executeBotTurn = async (gameId) => {
  const response = await axios.post(`${API}/games/${gameId}/bot-turn`);
  return response.data;
};

// Error handler wrapper
export const apiCall = async (apiFunction, ...args) => {
  try {
    return await apiFunction(...args);
  } catch (error) {
    console.error('API call failed:', error);
    throw new Error(error.response?.data?.detail || 'API call failed');
  }
};