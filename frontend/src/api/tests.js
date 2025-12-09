import api from './axios';

export const testsAPI = {
  // Get all tests
  getAllTests: async () => {
    const response = await api.get('/tests/');
    return response.data;
  },

  // Get a single test by ID
  getTest: async (testId) => {
    const response = await api.get(`/tests/${testId}/`);
    return response.data;
  },

  // Submit code for a test
  submitCode: async (testId, codeData) => {
    const response = await api.post(`/tests/${testId}/submit/`, codeData);
    return response.data;
  },

  // Execute code (run test cases)
  executeCode: async (codeData) => {
    const response = await api.post('/tests/execute/', codeData);
    return response.data;
  },

  // Get test cases for a test
  getTestCases: async (testId) => {
    const response = await api.get(`/tests/${testId}/testcases/`);
    return response.data;
  },

  // Save user's code progress
  saveProgress: async (testId, code) => {
    const response = await api.post(`/tests/${testId}/save/`, { code });
    return response.data;
  },

  // Get user's saved code
  getSavedCode: async (testId) => {
    const response = await api.get(`/tests/${testId}/saved/`);
    return response.data;
  },
};
