import { BrowserRouter, Routes, Route } from "react-router-dom";
import AppLayout from "./components/layout/AppLayout";
import Dashboard from "./pages/Dashboard";
import RegisterPage from "./pages/RegisterPage";
import StudentRegistry from "./pages/StudentRegistry";
import AttendanceGate from "./pages/AttendanceGate";
import StudentDetails from "./pages/StudentDetails";

// Import theme styles
import "./styles/theme.css";

function App() {
  return (
    <BrowserRouter>
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
    </BrowserRouter>
  );
}

export default App;
