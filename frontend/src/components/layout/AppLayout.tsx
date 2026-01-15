import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { removeAuthToken } from "../../api/api";
import logoImage from "../../assets/Lamitie_2k25_Logo_NoShadow.png";

interface AppLayoutProps {
  children: React.ReactNode;
}

// Navigation items
const navItems = [
  { path: "/", label: "Dashboard" },
  { path: "/register", label: "Register Student" },
  { path: "/archives", label: "Student List" },
  { path: "/gate", label: "Check Attendance" },
];

function AppLayout({ children }: AppLayoutProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    removeAuthToken();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-mordor">
      {/* Background Effects */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-[#1a1510]/40 via-transparent to-[#0a0a0a]/60" />
        <div className="absolute top-0 left-0 w-48 h-48 opacity-10">
          <svg viewBox="0 0 100 100" className="w-full h-full text-[#c5a059]">
            <path d="M0,0 L100,0 L100,20 Q50,50 20,100 L0,100 Z" fill="currentColor" />
          </svg>
        </div>
        <div className="absolute bottom-0 right-0 w-48 h-48 opacity-10 rotate-180">
          <svg viewBox="0 0 100 100" className="w-full h-full text-[#c5a059]">
            <path d="M0,0 L100,0 L100,20 Q50,50 20,100 L0,100 Z" fill="currentColor" />
          </svg>
        </div>
      </div>

      {/* ===== NAVBAR ===== */}
      <header className="fixed top-0 left-0 right-0 z-50 glass-dark border-b border-[#c5a059]/20">
        <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2 shrink-0">
              <img src={logoImage} alt="L'amitié" className="h-10 w-auto" />
              <span className="hidden sm:block font-display text-lg text-[#c5a059] tracking-wide">
                L'AMITIÉ 2K25
              </span>
            </Link>

            {/* Desktop Nav */}
            <nav className="hidden md:flex items-center gap-1">
              {navItems.map((item) => {
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`
                      px-4 py-2 rounded-lg font-display text-sm transition-all duration-200
                      ${isActive 
                        ? "bg-[#c5a059]/20 text-[#c5a059]" 
                        : "text-[#e8dcc4]/80 hover:text-[#c5a059] hover:bg-[#c5a059]/10"
                      }
                    `}
                  >
                    {item.label}
                  </Link>
                );
              })}
              {/* Logout Button */}
              <button
                onClick={handleLogout}
                className="px-4 py-2 rounded-lg font-display text-sm transition-all duration-200 text-red-400/80 hover:text-red-400 hover:bg-red-400/10 ml-2"
              >
                Logout
              </button>
            </nav>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-lg text-[#c5a059] hover:bg-[#c5a059]/10 transition-colors"
              aria-label="Menu"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu Dropdown */}
        {mobileMenuOpen && (
          <nav className="md:hidden border-t border-[#c5a059]/20 bg-[#0a0a0a]/98 backdrop-blur-lg">
            <div className="px-4 py-2">
              {navItems.map((item) => {
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`
                      flex items-center px-4 py-3 rounded-lg my-1 transition-all
                      ${isActive 
                        ? "bg-[#c5a059]/20 text-[#c5a059]" 
                        : "text-[#e8dcc4] hover:bg-[#c5a059]/10"
                      }
                    `}
                  >
                    <span className="font-display">{item.label}</span>
                  </Link>
                );
              })}
              {/* Mobile Logout Button */}
              <button
                onClick={() => {
                  setMobileMenuOpen(false);
                  handleLogout();
                }}
                className="flex items-center px-4 py-3 rounded-lg my-1 transition-all text-red-400 hover:bg-red-400/10 w-full"
              >
                <span className="font-display">Logout</span>
              </button>
            </div>
          </nav>
        )}
      </header>

      {/* ===== MAIN CONTENT ===== */}
      <main className="relative pt-16 min-h-screen flex justify-center">
        <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
          {children}
        </div>
      </main>

      {/* ===== FOOTER ===== */}
      <footer className="relative border-t border-[#c5a059]/10 py-6">
        <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-[#c5a059]/50 text-xs tracking-widest mb-2">
            ═══ ◆ L'AMITIÉ 2K25 ◆ ═══
          </p>
          <p className="text-[#c5a059]/50 text-xs font-body">
            Developed by Shaveen Udayanga
          </p>
        </div>
      </footer>
    </div>
  );
}

export default AppLayout;
