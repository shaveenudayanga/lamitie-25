import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getStudent } from "../api/api";

interface StudentData {
  id: number;
  name: string;
  index_number: string;
  combination: string;
  email: string;
  mobile_number?: string;
  attendance_status?: boolean;
  created_at?: string;
}

function StudentDetails() {
  const { indexNumber } = useParams<{ indexNumber: string }>();
  const [student, setStudent] = useState<StudentData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStudent = async () => {
      if (!indexNumber) return;
      
      try {
        const response = await getStudent(indexNumber);
        setStudent(response.data);
        setError(null);
      } catch (err: any) {
        console.error("Failed to fetch student:", err);
        setError(
          err?.response?.data?.detail?.detail ||
          "This scroll could not be found in the archives."
        );
      } finally {
        setLoading(false);
      }
    };
    fetchStudent();
  }, [indexNumber]);

  // Generate QR code URL (using a public QR code API)
  const qrCodeUrl = indexNumber
    ? `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(
        indexNumber
      )}&bgcolor=f5f0e1&color=3e2723`
    : null;

  if (loading) {
    return (
      <div className="w-full">
        <div className="card-dark text-center py-16 max-w-md mx-auto">
          <div className="inline-block animate-spin text-4xl mb-4">⏳</div>
          <p className="text-[#c5a059] font-display text-xl">
            Retrieving character scroll...
          </p>
        </div>
      </div>
    );
  }

  if (error || !student) {
    return (
      <div className="w-full">
        <header className="text-center mb-8 animate-fade-in-up">
          <h1 className="font-display text-3xl md:text-4xl text-[#c5a059] text-glow-gold tracking-wider mb-2">
            Scroll Not Found
          </h1>
          
          {/* Ornamental Divider */}
          <div className="divider-ornament max-w-sm mx-auto">
            <span>✦</span>
          </div>
        </header>
        
        <div className="card-dark text-center py-12 border-red-900/50 max-w-lg mx-auto">
          <span className="text-4xl mb-4 block">🔍</span>
          <p className="text-red-400 font-display text-xl mb-4">{error}</p>
          <p className="text-[#e8dcc4]/50 mb-6">
            The index "{indexNumber}" does not exist in our archives.
          </p>
          <Link to="/archives" className="btn-rune inline-block">
            Return to Archives
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full">
      {/* Page Header */}
      <header className="text-center mb-8 animate-fade-in-up">
        <h1 className="font-display text-3xl md:text-4xl text-[#c5a059] text-glow-gold tracking-wider mb-2">
          Character Sheet
        </h1>
        <p className="text-[#e8dcc4]/70 italic font-body">
          The scroll of {student.name}
        </p>
        
        {/* Ornamental Divider */}
        <div className="divider-ornament max-w-sm mx-auto">
          <span>✦</span>
        </div>
      </header>

      {/* Character Card */}
      <div className="card-scroll animate-fade-in-up max-w-2xl mx-auto" style={{ animationDelay: "0.2s" }}>
        <div className="grid md:grid-cols-2 gap-8">
          {/* Left: Info */}
          <div className="space-y-6">
            {/* Name */}
            <div>
              <label className="block text-[#3e2723]/60 text-sm font-display uppercase tracking-wider mb-1">
                Name
              </label>
              <p className="font-display text-2xl text-[#3e2723]">
                {student.name}
              </p>
            </div>

            {/* Index Number */}
            <div>
              <label className="block text-[#3e2723]/60 text-sm font-display uppercase tracking-wider mb-1">
                Index of Identification
              </label>
              <code className="text-[#800020] bg-[#800020]/10 px-3 py-1 rounded font-display text-xl">
                {student.index_number}
              </code>
            </div>

            {/* Combination */}
            <div>
              <label className="block text-[#3e2723]/60 text-sm font-display uppercase tracking-wider mb-1">
                Path of Study
              </label>
              <p className="text-[#3e2723] text-lg">{student.combination}</p>
            </div>

            {/* Email */}
            <div>
              <label className="block text-[#3e2723]/60 text-sm font-display uppercase tracking-wider mb-1">
                Raven Address
              </label>
              <p className="text-[#3e2723]/80 text-sm break-all">{student.email}</p>
            </div>

            {/* Mobile Number */}
            {student.mobile_number && (
              <div>
                <label className="block text-[#3e2723]/60 text-sm font-display uppercase tracking-wider mb-1">
                  Communication Crystal
                </label>
                <p className="text-[#3e2723]/80 text-sm">{student.mobile_number}</p>
              </div>
            )}

            {/* Status */}
            <div>
              <label className="block text-[#3e2723]/60 text-sm font-display uppercase tracking-wider mb-2">
                Fellowship Status
              </label>
              {student.attendance_status ? (
                <span className="inline-flex items-center gap-2 px-4 py-2 bg-green-800/20 border-2 border-green-600/50 rounded-lg text-green-700 font-display">
                  <span className="text-xl">✓</span>
                  <span>Present at the Gathering</span>
                </span>
              ) : (
                <span className="inline-flex items-center gap-2 px-4 py-2 bg-yellow-800/20 border-2 border-yellow-600/50 rounded-lg text-yellow-700 font-display">
                  <span className="text-xl">○</span>
                  <span>Awaiting Arrival</span>
                </span>
              )}
            </div>
          </div>

          {/* Right: QR Code */}
          <div className="flex flex-col items-center justify-center">
            <div className="p-4 bg-[#f5f0e1] rounded-xl border-2 border-[#c5a059]/50 shadow-lg">
              {qrCodeUrl && (
                <img
                  src={qrCodeUrl}
                  alt={`QR Code for ${student.index_number}`}
                  className="w-48 h-48"
                />
              )}
            </div>
            <p className="text-[#3e2723]/60 text-sm mt-3 text-center">
              Scan at the Gate
            </p>
            <p className="text-[#3e2723]/40 text-xs mt-1">
              {student.index_number}
            </p>
          </div>
        </div>

        {/* Divider */}
        <div className="flex items-center justify-center gap-3 py-6 text-[#c5a059]/50">
          <span>═══</span>
          <span>◆</span>
          <span>═══</span>
        </div>

        {/* Footer Quote */}
        <div className="text-center">
          <p className="text-[#3e2723]/50 text-sm italic">
            "A wizard is never late, nor is he early, he arrives precisely when he means to."
          </p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-wrap justify-center gap-4 mt-8 animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
        <Link to="/archives" className="btn-rune">
          ← Back to Archives
        </Link>
        <Link to="/gate" className="btn-rune">
          Mark Attendance →
        </Link>
      </div>

      {/* Bottom decoration */}
      <div className="text-center mt-8 text-[#c5a059]/30">
        <p className="text-sm tracking-[0.3em]">═══════ ◆ ═══════</p>
      </div>
    </div>
  );
}

export default StudentDetails;
