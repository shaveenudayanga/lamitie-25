import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, setAuthToken } from "../api/api";

const Login: React.FC = () => {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await login(password);
      setAuthToken(response.data.access_token);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Invalid password. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>L'amitié 2025</h1>
        <h2 style={styles.subtitle}>Admin Login</h2>
        
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter admin password"
              style={styles.input}
              required
            />
          </div>
          
          {error && <div style={styles.error}>{error}</div>}
          
          <button 
            type="submit" 
            style={styles.button}
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    minHeight: "100vh",
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    padding: "20px",
  },
  card: {
    background: "white",
    borderRadius: "16px",
    padding: "40px",
    boxShadow: "0 10px 40px rgba(0, 0, 0, 0.2)",
    width: "100%",
    maxWidth: "400px",
    textAlign: "center",
  },
  title: {
    fontSize: "28px",
    fontWeight: "bold",
    color: "#333",
    marginBottom: "8px",
  },
  subtitle: {
    fontSize: "18px",
    color: "#666",
    marginBottom: "30px",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "20px",
  },
  inputGroup: {
    textAlign: "left",
  },
  label: {
    display: "block",
    marginBottom: "8px",
    fontWeight: "500",
    color: "#333",
  },
  input: {
    width: "100%",
    padding: "12px 16px",
    fontSize: "16px",
    border: "2px solid #e0e0e0",
    borderRadius: "8px",
    outline: "none",
    transition: "border-color 0.3s",
    boxSizing: "border-box",
  },
  button: {
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    color: "white",
    border: "none",
    padding: "14px 24px",
    fontSize: "16px",
    fontWeight: "600",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "transform 0.2s, box-shadow 0.2s",
  },
  error: {
    background: "#fee",
    color: "#c00",
    padding: "12px",
    borderRadius: "8px",
    fontSize: "14px",
  },
};

export default Login;
