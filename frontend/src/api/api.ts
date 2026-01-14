import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

// GENERAL
export const welcome = () => API.get("/");

// REGISTRATION
export const registerStudent = (data: any) => API.post("/register", data);

// ATTENDANCE
export const scanAttendance = (data: any) => API.post("/scan", data);

// ADMIN
export const getStudents = () => API.get("/students");
export const getStudent = (index: any) => API.get(`/students/${index}`);
