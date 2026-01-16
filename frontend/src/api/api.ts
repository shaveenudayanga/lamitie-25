import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://20.120.179.111/api/v1",
});

// Add auth token to requests if available
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("auth_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 responses (unauthorized)
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login if unauthorized
      localStorage.removeItem("auth_token");
      // Optionally redirect to login page
      if (window.location.pathname !== "/") {
        window.location.href = "/";
      }
    }
    return Promise.reject(error);
  }
);

// AUTH
export const login = (password: string) => API.post("/auth/login", { password });
export const verifyToken = () => API.post("/auth/verify");

// Helper functions for token management
export const setAuthToken = (token: string) => {
  localStorage.setItem("auth_token", token);
};

export const getAuthToken = () => {
  return localStorage.getItem("auth_token");
};

export const removeAuthToken = () => {
  localStorage.removeItem("auth_token");
};

export const isAuthenticated = () => {
  return !!localStorage.getItem("auth_token");
};

// GENERAL
export const welcome = () => API.get("/");

// REGISTRATION (Protected)
export const registerStudent = (data: any) => API.post("/users/register/", data);

// ATTENDANCE (Protected)
export const scanAttendance = (data: any) => API.post("/registrations/scan/", data);

// ADMIN (Protected)
export const getStudents = () => API.get("/users/");
export const getStudent = (index: any) => API.get(`/users/index/${index}/`);
export const updateStudent = (index: string, data: any) => API.put(`/users/index/${index}/`, data);
