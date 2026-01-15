import { useState, useEffect, useRef } from "react";
import { scanAttendance, getStudent } from "../api/api";

type ScanStatus = "idle" | "scanning" | "success" | "error";

interface ScanResult {
  status: ScanStatus;
  message: string;
  studentName?: string;
}

function AttendanceGate() {
  const [manualIndex, setManualIndex] = useState("");
  const [loading, setLoading] = useState(false);
  const [scanResult, setScanResult] = useState<ScanResult>({
    status: "idle",
    message: "",
  });
  const [useCamera, setUseCamera] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Reset status after showing result
  useEffect(() => {
    if (scanResult.status === "success" || scanResult.status === "error") {
      const timer = setTimeout(() => {
        setScanResult({ status: "idle", message: "" });
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [scanResult.status]);

  // Camera setup for QR scanning
  useEffect(() => {
    if (useCamera && videoRef.current) {
      navigator.mediaDevices
        .getUserMedia({ video: { facingMode: "environment" } })
        .then((stream) => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
          }
        })
        .catch((err) => {
          console.error("Camera error:", err);
          setUseCamera(false);
          setScanResult({
            status: "error",
            message: "Cannot access camera. Please use manual entry.",
          });
        });
    }

    return () => {
      if (videoRef.current?.srcObject) {
        const tracks = (videoRef.current.srcObject as MediaStream).getTracks();
        tracks.forEach((track) => track.stop());
      }
    };
  }, [useCamera]);

  // Handle manual entry submission
  const handleManualSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!manualIndex.trim()) return;

    setLoading(true);
    setScanResult({ status: "scanning", message: "Verifying credentials..." });

    try {
      // First check if student exists
      const studentRes = await getStudent(manualIndex.trim());
      const studentName = studentRes.data?.name || "Unknown";

      // Then mark attendance
      const res = await scanAttendance({ index_number: manualIndex.trim() });

      if (res.data?.success) {
        setScanResult({
          status: "success",
          message: res.data.message || "Access Granted!",
          studentName: studentName,
        });
        setManualIndex("");
      } else {
        setScanResult({
          status: "error",
          message: res.data?.message || "You Shall Not Pass!",
        });
      }
    } catch (err: any) {
      const errorMsg =
        err?.response?.data?.detail?.detail ||
        err?.response?.data?.detail ||
        "You Shall Not Pass!";
      setScanResult({
        status: "error",
        message: errorMsg,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full">
      {/* Page Header */}
      <header className="text-center mb-8 animate-fade-in-up">
        <h1 className="font-display text-3xl md:text-4xl text-[#c5a059] text-glow-gold tracking-wider mb-2">
          The Gate
        </h1>
        <p className="text-[#e8dcc4]/70 italic font-body text-lg md:text-xl">
          "Speak, friend, and enter"
        </p>
        
        {/* Elvish subtitle */}
        <p className="text-[#c5a059]/40 text-sm mt-2 tracking-wider">
          Mellon
        </p>
        
        {/* Ornamental Divider */}
        <div className="divider-ornament max-w-sm mx-auto">
          <span>⚔</span>
        </div>
      </header>

      {/* Status Display - Large Visual */}
      {scanResult.status !== "idle" && (
        <div
          className={`
            mb-8 p-8 rounded-2xl text-center animate-fade-in-up
            ${scanResult.status === "success" ? "status-granted" : ""}
            ${scanResult.status === "error" ? "status-denied" : ""}
            ${scanResult.status === "scanning" ? "glass-gold animate-pulse" : ""}
          `}
        >
          {scanResult.status === "success" && (
            <>
              <span className="text-7xl block mb-4">✓</span>
              <h2 className="font-display text-4xl text-green-400 text-glow-gold mb-2">
                ACCESS GRANTED
              </h2>
              {scanResult.studentName && (
                <p className="text-green-300 text-xl font-body">
                  Welcome, {scanResult.studentName}!
                </p>
              )}
              <p className="text-green-400/70 mt-2">{scanResult.message}</p>
            </>
          )}

          {scanResult.status === "error" && (
            <>
              <span className="text-7xl block mb-4">🛑</span>
              <h2 className="font-display text-4xl text-red-400 mb-2">
                YOU SHALL NOT PASS!
              </h2>
              <p className="text-red-300 text-lg">{scanResult.message}</p>
            </>
          )}

          {scanResult.status === "scanning" && (
            <>
              <span className="text-5xl block mb-4 animate-spin">⏳</span>
              <h2 className="font-display text-2xl text-[#c5a059]">
                {scanResult.message}
              </h2>
            </>
          )}
        </div>
      )}

      {/* Entry Methods */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Manual Entry */}
        <div className="card-scroll animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
          <div className="text-center mb-6">
            <span className="text-4xl mb-3 block">✍️</span>
            <h3 className="font-display text-xl text-[#3e2723]">
              Manual Entry
            </h3>
            <p className="text-[#3e2723]/60 text-sm">
              Inscribe thy index number
            </p>
          </div>

          <form onSubmit={handleManualSubmit} className="space-y-4">
            <div className="flex items-center justify-center gap-2">
              <span className="text-[#3e2723] font-display text-2xl font-semibold">AS2023</span>
              <input
                type="text"
                value={manualIndex.replace("AS2023", "")}
                onChange={(e) => {
                  const value = e.target.value.replace(/\D/g, "").slice(0, 3);
                  setManualIndex("AS2023" + value);
                }}
                placeholder="605"
                maxLength={3}
                className="flex-1 bg-transparent border-b-2 border-[#c5a059]/50 
                           text-[#3e2723] placeholder-[#3e2723]/40 text-center
                           py-3 px-2 font-display text-2xl tracking-wider
                           focus:outline-none focus:border-[#c5a059]
                           transition-all duration-300"
              />
            </div>
            
            <button
              type="submit"
              disabled={loading || !manualIndex.trim()}
              className="btn-rune w-full"
            >
              {loading ? "Verifying..." : "Enter the Gate"}
            </button>
          </form>
        </div>

        {/* QR Scanner */}
        <div className="card-dark animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
          <div className="text-center mb-6">
            <span className="text-4xl mb-3 block">📷</span>
            <h3 className="font-display text-xl text-[#c5a059]">
              QR Scan
            </h3>
            <p className="text-[#e8dcc4]/60 text-sm">
              Present thy invitation scroll
            </p>
          </div>

          {useCamera ? (
            <div className="space-y-4">
              <div className="relative aspect-square bg-black rounded-lg overflow-hidden border-2 border-[#c5a059]/50">
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  className="w-full h-full object-cover"
                />
                {/* Scanner overlay */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-48 h-48 border-2 border-[#c5a059] rounded-lg animate-pulse" />
                </div>
              </div>
              <canvas ref={canvasRef} className="hidden" />
              <button
                onClick={() => setUseCamera(false)}
                className="w-full py-2 text-[#c5a059] border border-[#c5a059]/50 rounded-lg
                           hover:bg-[#c5a059]/10 transition-colors"
              >
                Close Scanner
              </button>
              <p className="text-[#c5a059]/50 text-xs text-center">
                Note: For full QR scanning, install react-qr-reader package
              </p>
            </div>
          ) : (
            <div className="text-center py-8">
              <div className="w-32 h-32 mx-auto mb-4 border-2 border-dashed border-[#c5a059]/30 rounded-lg flex items-center justify-center">
                <span className="text-4xl opacity-50">📱</span>
              </div>
              <button
                onClick={() => setUseCamera(true)}
                className="btn-rune"
              >
                Activate Scanner
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Instructions */}
      <div className="mt-8 card-dark text-center animate-fade-in-up" style={{ animationDelay: "0.4s" }}>
        <h4 className="font-display text-lg text-[#c5a059] mb-4">
          📜 Instructions for the Gatekeeper
        </h4>
        <div className="grid md:grid-cols-3 gap-4 text-sm text-[#e8dcc4]/70">
          <div className="p-4">
            <span className="text-2xl block mb-2">1️⃣</span>
            <p>Ask the guest for their Index Number or Invitation QR</p>
          </div>
          <div className="p-4">
            <span className="text-2xl block mb-2">2️⃣</span>
            <p>Enter the number or scan the QR code above</p>
          </div>
          <div className="p-4">
            <span className="text-2xl block mb-2">3️⃣</span>
            <p>Wait for ACCESS GRANTED before allowing entry</p>
          </div>
        </div>
      </div>

      {/* Bottom decoration */}
      <div className="text-center mt-8 text-[#c5a059]/30">
        <p className="text-sm tracking-[0.3em]">═══════ ◆ ═══════</p>
      </div>
    </div>
  );
}

export default AttendanceGate;
