import { BrowserRouter, Routes, Route } from "react-router-dom";
import AppLayout from "./components/layout/AppLayout";
import ProtectedRoute from "./components/ProtectedRoute";
import Dashboard from "./pages/Dashboard";
import RegisterPage from "./pages/RegisterPage";
import StudentRegistry from "./pages/StudentRegistry";
import AttendanceGate from "./pages/AttendanceGate";
import StudentDetails from "./pages/StudentDetails";
import Login from "./pages/Login";

// Import theme styles
import "./styles/theme.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Login Route */}
        <Route path="/login" element={<Login />} />
        
        {/* Protected Routes */}
        <Route path="/*" element={
          <ProtectedRoute>
            <AppLayout>
              <Routes>
                {/* Home / Dashboard - "The Shire" */}
                <Route path="/" element={<Dashboard />} />
                
                {/* Registration - "The Scroll of Entry" */}
                <Route path="/register" element={<RegisterPage />} />
                
                {/* Student Registry - "The Archives" */}
                <Route path="/archives" element={<StudentRegistry />} />
                
                {/* Attendance Gate - "Speak Friend and Enter" */}
                <Route path="/gate" element={<AttendanceGate />} />
                
                {/* Student Details - "Character Sheet" */}
                <Route path="/student/:indexNumber" element={<StudentDetails />} />
              </Routes>
            </AppLayout>
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
