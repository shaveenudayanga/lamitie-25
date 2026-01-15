import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getStudents } from "../api/api";

interface Student {
  id: number;
  name: string;
  index_number: string;
  combination: string;
  email: string;
  is_attended?: boolean;
  created_at?: string;
}

function StudentRegistry() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await getStudents();
        setStudents(response.data || []);
        setError(null);
      } catch (err) {
        console.error("Failed to fetch students:", err);
        setError("Failed to load student records. Please try again.");
      } finally {
        setLoading(false);
      }
    };
    fetchStudents();
  }, []);

  // Filter students based on search query
  const filteredStudents = students.filter(
    (student) =>
      student.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      student.index_number.toLowerCase().includes(searchQuery.toLowerCase()) ||
      student.combination.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="w-full">
      {/* Page Header */}
      <section className="text-center mb-8 animate-fade-in-up">
        <h1 className="font-display text-3xl md:text-4xl text-[#c5a059] text-glow-gold tracking-wider mb-2">
          The Archives
        </h1>
        <p className="text-[#e8dcc4]/70 italic font-body">
          "In the land of Mordor where the records lie" — The Fellowship Roster
        </p>
        
        {/* Ornamental Divider */}
        <div className="divider-ornament max-w-sm mx-auto">
          <span>✦</span>
        </div>
      </section>

      {/* Search Section */}
      <section className="mb-8">
        <div className="card-dark max-w-2xl mx-auto animate-fade-in-up" style={{ animationDelay: "0.1s" }}>
        <div className="flex items-center gap-4">
          <span className="text-2xl">🔍</span>
          <div className="flex-1">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by name, index, or combination..."
              className="w-full bg-transparent border-b-2 border-[#c5a059]/30 
                         text-[#e8dcc4] placeholder-[#c5a059]/40
                         py-3 px-2 font-body text-lg
                         focus:outline-none focus:border-[#c5a059]
                         transition-all duration-300"
            />
          </div>
        </div>
        </div>
      </section>

      {/* Stats Bar */}
      <div className="flex flex-wrap justify-center gap-6 mb-8 animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
        <div className="glass-dark px-6 py-3 rounded-lg">
          <span className="text-[#c5a059]/60 text-sm">Total Registered:</span>
          <span className="ml-2 text-[#c5a059] font-display text-xl">{students.length}</span>
        </div>
        <div className="glass-dark px-6 py-3 rounded-lg">
          <span className="text-[#c5a059]/60 text-sm">Showing:</span>
          <span className="ml-2 text-[#c5a059] font-display text-xl">{filteredStudents.length}</span>
        </div>
      </div>

      {/* Content Area */}
      <div className="animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
        {loading ? (
          /* Loading State */
          <div className="card-dark text-center py-16 max-w-md mx-auto">
            <div className="inline-block animate-spin text-4xl mb-4">⏳</div>
            <p className="text-[#c5a059] font-display text-xl">
              Loading student records...
            </p>
          </div>
        ) : error ? (
          /* Error State */
          <div className="card-dark text-center py-16 border-red-900/50 max-w-md mx-auto">
            <span className="text-4xl mb-4 block">⚠️</span>
            <p className="text-red-400 font-display text-xl mb-2">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="btn-rune mt-4"
            >
              Try Again
            </button>
          </div>
        ) : filteredStudents.length === 0 ? (
          /* Empty State */
          <div className="card-dark text-center py-16 max-w-md mx-auto">
            <span className="text-4xl mb-4 block">📭</span>
            <p className="text-[#c5a059] font-display text-xl mb-2">
              {searchQuery
                ? "No matching records found"
                : "No registrations yet"}
            </p>
            <p className="text-[#e8dcc4]/50 text-sm">
              {searchQuery
                ? "Try a different search term..."
                : "No students have registered yet"}
            </p>
          </div>
        ) : (
          /* Data Table - Ledger Style */
          <div className="card-dark overflow-hidden max-w-5xl mx-auto">
            <div className="overflow-x-auto">
              <table className="table-ledger">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Name</th>
                    <th>Index</th>
                    <th>Combination</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredStudents.map((student, index) => (
                    <tr key={student.id} className="group">
                      <td className="text-[#c5a059]/50">{index + 1}</td>
                      <td>
                        <div className="font-display text-[#e8dcc4]">
                          {student.name}
                        </div>
                      </td>
                      <td>
                        <code className="text-[#c5a059] bg-[#c5a059]/10 px-2 py-1 rounded">
                          {student.index_number}
                        </code>
                      </td>
                      <td className="text-[#e8dcc4]/70">{student.combination}</td>
                      <td>
                        {student.is_attended ? (
                          <span className="inline-flex items-center gap-1 px-3 py-1 bg-green-900/30 border border-green-500/30 rounded-full text-green-400 text-sm">
                            <span>✓</span> Arrived
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 px-3 py-1 bg-yellow-900/30 border border-yellow-500/30 rounded-full text-yellow-400 text-sm">
                            <span>○</span> Awaited
                          </span>
                        )}
                      </td>
                      <td>
                        <Link
                          to={`/student/${student.index_number}`}
                          className="inline-flex items-center gap-2 text-[#c5a059] hover:text-[#d4b068] transition-colors"
                        >
                          <span>View</span>
                          <span>→</span>
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* Bottom decoration */}
      <section className="text-center mt-8">
        <p className="text-sm tracking-[0.3em] text-[#c5a059]/50">═══════ ◆ ═══════</p>
      </section>
    </div>
  );
}

export default StudentRegistry;
