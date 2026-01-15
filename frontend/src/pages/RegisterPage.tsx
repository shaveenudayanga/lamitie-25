import { useState, type ChangeEvent, type FormEvent, useEffect, useRef } from "react";
import { registerStudent } from "../api/api";

interface StudentForm {
  name: string;
  index_number: string;
  combination: string;
  email: string;
}

const combinations = [
  // Physical Science
  "MAT/CS/STA",
  "MAT/CS/PHY",
  "MAT/STA/PHY",
  "MAT/STA/ECON",
  "MAT/STA/CHE",
  "MAT/CHE/MAN",
  "MAT/CHE/PHY",
  "MAT/CS/AMT",
  "MAT/AMT/MAN",
  "MAT/PHY/ICT",
  "MAT/PHY/EES",

  // Common Combination
  "POLYMER/PHY/CHE",
  "FORESTRY/CHE/MAN",

  // Biological Combination
  "CHE/BIO/GMB",
  "CHE/EMF/GMB",
  "CHE/BIO/FSC",
  "CHE/ZOO/MBL",
  "CHE/ZOO/PBT",
  "CHE/EMF/PBT",
  "CHE/ZOO/ARM",
  "CHE/MAN/ARM",
  "CHE/EMF/ARM",
  "CHE/ZOO/MAN",
  "CHE/MAN/EMF",

  // Additional Fields
  "Food Science",
  "Sport Science",
];

function RegisterPage() {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [combinationSearch, setCombinationSearch] = useState("");
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const [form, setForm] = useState<StudentForm>({
    name: "",
    index_number: "",
    email: "",
    combination: "",
  });

  // Filter combinations based on search
  const filteredCombinations = combinations.filter((combo) =>
    combo.toLowerCase().includes(combinationSearch.toLowerCase())
  );

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSuccess(false);
    console.log("form", form);
    try {
      const res = await registerStudent(form);

      // SUCCESS
      if (res.data.success) {
        setSuccess(true);
        alert(res.data.message);

        setForm({
          name: "",
          index_number: "",
          email: "",
          combination: "",
        });
      }
    } catch (err: any) {
      // Axios error handling
      const errorData = err?.response?.data;

      if (errorData?.detail?.success === false) {
        alert(errorData.detail.detail);
      } else {
        alert("Something went wrong. Please try again.");
      }

      console.error("Registration error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  return (
    <div className="w-full">
      {/* Page Header */}
      <section className="text-center mb-8 animate-fade-in-up">
        <h1 className="font-display text-3xl md:text-4xl text-[#c5a059] text-glow-gold tracking-wider mb-2">
          The Scroll of Entry
        </h1>
        <p className="text-[#e8dcc4]/70 italic font-body">
          "Speak friend, and enter" — Inscribe your name upon the Fellowship roster
        </p>
        
        {/* Ornamental Divider */}
        <div className="divider-ornament max-w-sm mx-auto">
          <span>✦</span>
        </div>
      </section>

      {/* Registration Form - Scroll Style */}
      <section>
        <div className="card-scroll max-w-lg mx-auto animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
        {/* Scroll Header */}
        <div className="text-center mb-8">
          <h2 className="font-display text-2xl text-[#3e2723] mb-2">
            Student Registration
          </h2>
          <p className="text-[#3e2723]/60 text-sm">
            Fill in the details below
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Name Field */}
          <div className="space-y-2">
            <label className="block text-[#3e2723]/70 text-sm font-display uppercase tracking-wider">
              Full Name
            </label>
            <input
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="Enter first and last name (e.g., Mahinda Rajapasksa)"
              required
              className="w-full bg-transparent border-b-2 border-[#c5a059]/50 
                         text-[#3e2723] placeholder-[#3e2723]/40
                         py-3 px-2 font-body text-lg
                         focus:outline-none focus:border-[#c5a059]
                         transition-all duration-300"
            />
          </div>

          {/* Index Number Field */}
          <div className="space-y-2">
            <label className="block text-[#3e2723]/70 text-sm font-display uppercase tracking-wider">
              Index Number
            </label>
            <div className="flex items-center gap-2">
              <span className="text-[#3e2723] font-body text-lg font-semibold">AS2023</span>
              <input
                type="text"
                name="index_number"
                value={form.index_number.replace("AS2023", "")}
                onChange={(e) => {
                  const value = e.target.value.replace(/\D/g, "").slice(0, 3);
                  setForm({ ...form, index_number: "AS2023" + value });
                }}
                placeholder="605 (result: AS2023605)"
                maxLength={3}
                required
                className="flex-1 bg-transparent border-b-2 border-[#c5a059]/50 
                           text-[#3e2723] placeholder-[#3e2723]/40
                           py-3 px-2 font-body text-lg
                           focus:outline-none focus:border-[#c5a059]
                           transition-all duration-300"
              />
            </div>
          </div>

          {/* Combination Field */}
          <div className="space-y-2">
            <label className="block text-[#3e2723]/70 text-sm font-display uppercase tracking-wider">
              Combination
            </label>
            <div className="relative" ref={dropdownRef}>
              <input
                type="text"
                value={combinationSearch}
                onChange={(e) => {
                  setCombinationSearch(e.target.value);
                  setShowDropdown(true);
                }}
                onFocus={() => setShowDropdown(true)}
                placeholder="Type to search combinations..."
                className="w-full bg-[#f5f0e1] border-2 border-[#c5a059]/50 
                           text-[#3e2723] placeholder-[#3e2723]/40
                           py-3 px-2 font-body text-lg
                           rounded-md
                           focus:outline-none focus:border-[#c5a059]
                           transition-all duration-300"
              />
              
              {/* Hidden input to store actual value for form submission */}
              <input
                type="hidden"
                name="combination"
                value={form.combination}
                required
              />
              
              {/* Dropdown List */}
              {showDropdown && filteredCombinations.length > 0 && (
                <div className="absolute z-10 w-full mt-1 bg-[#f5f0e1] border-2 border-[#c5a059]/50 rounded-md shadow-lg max-h-60 overflow-y-auto">
                  {filteredCombinations.map((combo) => (
                    <div
                      key={combo}
                      onClick={() => {
                        setForm({ ...form, combination: combo });
                        setCombinationSearch(combo);
                        setShowDropdown(false);
                      }}
                      className="px-4 py-3 cursor-pointer hover:bg-[#c5a059]/20 text-[#3e2723] font-body transition-colors"
                    >
                      {combo}
                    </div>
                  ))}
                </div>
              )}
              
              {/* No results message */}
              {showDropdown && combinationSearch && filteredCombinations.length === 0 && (
                <div className="absolute z-10 w-full mt-1 bg-[#f5f0e1] border-2 border-[#c5a059]/50 rounded-md shadow-lg p-4 text-center text-[#3e2723]/60">
                  No matching combinations found
                </div>
              )}
            </div>
          </div>

          {/* Email Field */}
          <div className="space-y-2">
            <label className="block text-[#3e2723]/70 text-sm font-display uppercase tracking-wider">
              Email Address
            </label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              placeholder="your.email@example.com"
              required
              className="w-full bg-transparent border-b-2 border-[#c5a059]/50 
                         text-[#3e2723] placeholder-[#3e2723]/40
                         py-3 px-2 font-body text-lg
                         focus:outline-none focus:border-[#c5a059]
                         transition-all duration-300"
            />
          </div>

          {/* Divider */}
          <div className="flex items-center justify-center gap-3 py-4 text-[#c5a059]/50">
            <span>═══</span>
            <span>◆</span>
            <span>═══</span>
          </div>

          {/* Submit Button - Wax Seal Style */}
          <div className="text-center">
            <button
              type="submit"
              disabled={loading}
              className="btn-rune w-full max-w-xs mx-auto block"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                      fill="none"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  Submitting...
                </span>
              ) : (
                "Register"
              )}
            </button>
          </div>

          {/* Success Message */}
          {success && (
            <div className="mt-4 p-4 bg-green-900/20 border border-green-500/50 rounded-lg text-center">
              <span className="text-2xl block mb-2">✓</span>
              <p className="text-green-400 font-display">
                Registration successful!
              </p>
              <p className="text-green-400/70 text-sm mt-1">
                Check your email for the invitation.
              </p>
            </div>
          )}
        </form>

        {/* Footer note */}
        <div className="mt-8 pt-4 border-t border-[#c5a059]/30 text-center">
          <p className="text-[#3e2723]/50 text-sm italic">
            "Even the smallest person can change the course of the future."
          </p>
        </div>
        </div>
      </section>

      {/* Bottom decoration */}
      <section className="text-center mt-8">
        <p className="text-sm tracking-[0.3em] text-[#c5a059]/50">═══════ ◆ ═══════</p>
      </section>
    </div>
  );
}

export default RegisterPage;
