import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://20.120.179.111/api/v1",
});

// GENERAL
export const welcome = () => API.get("/");

// REGISTRATION
export const registerStudent = (data: any) => API.post("/users/register/", data);

// ATTENDANCE
export const scanAttendance = (data: any) => API.post("/registrations/scan/", data);

// ADMIN
export const getStudents = () => API.get("/users/");
export const getStudent = (index: any) => API.get(`/users/${index}/`);
