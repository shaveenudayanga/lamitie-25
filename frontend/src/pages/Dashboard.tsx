import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getStudents } from "../api/api";

// Navigation cards for the dashboard
const destinations = [
  {
    path: "/register",
    title: "Register Student",
    subtitle: "Add New Registration",
    icon: "�",
    description: "Register a new student for the L'amitié 2K25 event.",
    color: "from-amber-900/30 to-amber-800/20",
  },
  {
    path: "/archives",
    title: "Student List",
    subtitle: "View All Registrations",
    icon: "�",
    description: "View and search all registered students for the event.",
    color: "from-emerald-900/30 to-emerald-800/20",
  },
  {
    path: "/gate",
    title: "Mark Attendance",
    subtitle: "Scan QR Codes",
    icon: "✓",
    description: "Scan student QR codes to mark attendance at the event.",
    color: "from-purple-900/30 to-purple-800/20",
  },
];

function Dashboard() {
  const [stats, setStats] = useState({
    totalRegistered: 0,
    loading: true,
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await getStudents();
        setStats({
          totalRegistered: response.data?.length || 0,
          loading: false,
        });
      } catch (error) {
        console.error("Failed to fetch stats:", error);
        setStats({ totalRegistered: 0, loading: false });
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="w-full">
      {/* Hero Section */}
      <section className="text-center py-8 md:py-12 animate-fade-in-up">
        {/* Main Title */}
        <h1 className="font-display text-4xl md:text-6xl text-[#c5a059] text-glow-gold tracking-wider mb-4">
          L'AMITIÉ 2K25
        </h1>
        
        {/* Subtitle */}
        <p className="text-[#e8dcc4] text-xl md:text-2xl font-body italic mb-2">
          A Fellowship of Science
        </p>
        
        {/* Tagline */}
        <p className="text-[#c5a059]/60 text-sm tracking-[0.3em] uppercase">
          Faculty of Applied Sciences • University of Sri Jayewardenepura
        </p>

        {/* Ornamental Divider */}
        <div className="divider-ornament max-w-md mx-auto">
          <span className="text-2xl">⚔</span>
        </div>

        {/* Event Quote */}
        <blockquote className="max-w-2xl mx-auto">
          <p className="text-[#e8dcc4]/80 text-lg font-body italic">
            "The world is changed. I feel it in the water. I feel it in the earth.
            I smell it in the air. Much that once was is lost..."
          </p>
          <p className="text-[#c5a059]/50 text-sm mt-2">
            — But tonight, we gather to celebrate our fellowship!
          </p>
        </blockquote>
      </section>

      {/* Stats Section */}
      <section className="mb-12">
        <div className="card-dark max-w-md mx-auto text-center">
          <p className="text-[#c5a059]/60 text-sm uppercase tracking-[0.2em] font-display mb-2">
            Total Registrations
          </p>
          <div className="flex items-center justify-center gap-4">
            <span className="text-4xl">👥</span>
            <span className="font-display text-5xl text-[#c5a059] text-glow-gold">
              {stats.loading ? (
                <span className="animate-pulse">...</span>
              ) : (
                stats.totalRegistered
              )}
            </span>
            <span className="text-[#e8dcc4]/60 text-lg">students</span>
          </div>
          <p className="text-[#c5a059]/40 text-xs mt-2 italic">
            Registered for L'amitié 2K25
          </p>
        </div>
      </section>

      {/* Navigation Cards */}
      <section className="grid md:grid-cols-3 gap-6 mb-12">
        {destinations.map((dest, index) => (
          <Link
            key={dest.path}
            to={dest.path}
            className="group animate-fade-in-up"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div
              className={`
                card-dark h-full
                bg-gradient-to-br ${dest.color}
                hover:glow-gold-intense
                transition-all duration-500
                hover:-translate-y-2
              `}
            >
              {/* Title */}
              <h3 className="font-display text-xl text-[#c5a059] mb-1">
                {dest.title}
              </h3>
              
              {/* Subtitle */}
              <p className="text-[#c5a059]/50 text-sm italic mb-3">
                {dest.subtitle}
              </p>

              {/* Description */}
              <p className="text-[#e8dcc4]/70 text-sm font-body">
                {dest.description}
              </p>

              {/* Arrow indicator */}
              <div className="mt-4 flex items-center gap-2 text-[#c5a059]/50 group-hover:text-[#c5a059] transition-colors">
                <span className="text-sm">Go</span>
                <span className="group-hover:translate-x-2 transition-transform">→</span>
              </div>
            </div>
          </Link>
        ))}
      </section>

      {/* Event Details */}
      <section className="card-scroll max-w-2xl mx-auto text-center">
        <h2 className="font-display text-2xl text-[#3e2723] mb-6">
          📍 Event Details
        </h2>
        
        <div className="space-y-4 text-[#3e2723]/80">
          <div className="flex items-center justify-center gap-3">
            <span className="text-2xl">📅</span>
            <span className="font-display text-lg">25th January 2026</span>
          </div>
          
          <div className="flex items-center justify-center gap-3">
            <span className="text-2xl">🕐</span>
            <span className="font-display text-lg">1.00 P.M Onwards</span>
          </div>
          
          <div className="flex items-center justify-center gap-3">
            <span className="text-2xl">🏰</span>
            <span className="font-display text-lg">Willuda Inn, Godagama</span>
          </div>
        </div>

        {/* Decorative bottom */}
        <div className="mt-6 pt-4 border-t border-[#c5a059]/30">
          <p className="text-[#3e2723]/60 text-sm italic">
            "All we have to decide is what to do with the time that is given us."
          </p>
        </div>
      </section>

      {/* Footer decoration */}
      <div className="text-center mt-12 text-[#c5a059]/30">
        <p className="text-sm tracking-[0.3em]">═══════ ◆ ═══════</p>
      </div>
    </div>
  );
}

export default Dashboard;
