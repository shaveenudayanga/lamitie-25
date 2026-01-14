import { useState, type ChangeEvent, type FormEvent } from "react";
import { registerStudent } from "../api/api";
import Input from "../components/Input";
import Button from "../components/Button";

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

function Register() {
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState<StudentForm>({
    name: "",
    index_number: "",
    email: "",
    combination: "",
  });

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    console.log("form", form);
    try {
      const res = await registerStudent(form);

      // SUCCESS
      if (res.data.success) {
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

  const fieldClass = `
  w-full
  p-3
  rounded-xl

  bg-gray-800

  text-yellow-100
  placeholder-yellow-400/60

  border
  border-yellow-400/40

  shadow-inner
  shadow-black/40

  focus:outline-none
  focus:ring-2
  focus:ring-yellow-500/70
  focus:border-yellow-400

  transition-all
  duration-300
`;

  return (
    <div className="flex items-center justify-center">
      <form
        className="bg-gradient-to-br from-yellow-100/10 via-yellow-200/10 to-yellow-100/10 backdrop-blur-md border border-yellow-300/40 p-8 rounded-2xl shadow-2xl w-full max-w-md space-y-5"
        onSubmit={handleSubmit}
      >
        <h2 className="text-2xl font-extrabold text-yellow-600 text-center mb-4 tracking-wider drop-shadow-lg">
          Register
        </h2>

        <Input
          name="name"
          value={form.name}
          placeholder="Name"
          className={fieldClass}
          onChange={handleChange}
          required
        />

        <Input
          name="index_number"
          value={form.index_number}
          placeholder="Index Number"
          className={fieldClass}
          onChange={handleChange}
          required
        />

        <div
          className="bg-gray-800 rounded-lg focus-within:ring-2 focus-within:ring-yellow-500 px-1.5 border
                    border-yellow-400/40"
        >
          <select
            name="combination"
            value={form.combination}
            onChange={handleChange}
            className="w-full p-3 bg-gray-800 rounded-xl outline-none appearance-none text-yellow-100 font-normal invalid:text-yellow-400/60 invalid:font-normal focus:text-yellow-100 transition"
            required
          >
            <option
              className="text-yellow-400/60 font-normal"
              value=""
              disabled
            >
              Select Combination
            </option>
            {combinations.map((combo) => (
              <option key={combo} value={combo}>
                {combo}
              </option>
            ))}
          </select>
        </div>

        <Input
          name="email"
          value={form.email}
          placeholder="Email"
          className={fieldClass}
          onChange={handleChange}
          required
        />

        <Button
          disabled={loading}
          className=" w-full
    py-3
    rounded-xl
    font-extrabold
    tracking-widest
    uppercase
    text-yellow-300

    bg-gradient-to-r
    from-yellow-700
    via-yellow-500
    to-yellow-700

    border
    border-yellow-400/60

    shadow-lg
    shadow-yellow-500/30

    hover:from-yellow-600
    hover:via-yellow-400
    hover:to-yellow-600
    hover:shadow-yellow-400/60

    active:scale-95

    transition-all
    duration-300
    ease-out"
        >
          {loading ? "Registering..." : "Register"}
        </Button>
      </form>
    </div>
  );
}

export default Register;
