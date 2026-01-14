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
  const [form, setForm] = useState<StudentForm>({
    name: "",
    index_number: "",
    email: "",
    combination: "",
  });

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    console.log("form", form);

    // await registerStudent(form);
    alert("Registered successfully");
  };

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const fieldClass =
    "w-full p-3 bg-gray-800 text-yellow-100 placeholder-yellow-300 rounded-lg border border-yellow-300/40 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 outline-none";

  return (
    <div className="flex items-center justify-center">
      <form
        className="bg-gradient-to-br from-yellow-100/10 via-yellow-200/10 to-yellow-100/10 backdrop-blur-md border border-yellow-300/40 p-8 rounded-2xl shadow-2xl w-full max-w-md space-y-5"
        onSubmit={handleSubmit}
      >
        <h2 className="text-2xl font-extrabold text-yellow-300 text-center mb-4 tracking-wider drop-shadow-lg">
          Register
        </h2>

        <Input
          name="name"
          placeholder="Name"
          className={fieldClass}
          onChange={handleChange}
        />

        <Input
          name="index_number"
          placeholder="Index Number"
          className={fieldClass}
          onChange={handleChange}
        />

        <div className="bg-gray-800 rounded-lg focus-within:ring-2 focus-within:ring-yellow-500 px-1.5">
          <select
            name="combination"
            value={form.combination}
            onChange={handleChange}
            className="w-full p-3 bg-gray-800 text-yellow-100 placeholder-yellow-300 rounded-lg outline-none appearance-none"
          >
            <option value="" disabled>
              -- Select Combination --
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
          placeholder="Email"
          className="bg-gray-800 text-yellow-100 placeholder-yellow-300 focus:ring-yellow-500 focus:border-yellow-500"
          onChange={handleChange}
        />

        <Button className="w-full bg-yellow-400 hover:bg-yellow-500 text-gray-900 font-bold py-3 rounded-lg shadow-lg transition-all duration-300">
          Register
        </Button>
      </form>
    </div>
  );
}

export default Register;
