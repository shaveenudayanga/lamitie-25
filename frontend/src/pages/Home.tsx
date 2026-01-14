import { useEffect, useState } from "react";
import { welcome } from "../api/api";

function Home() {
  const [msg, setMsg] = useState("");

  useEffect(() => {
    welcome().then((res) => setMsg(res.data.message));
  }, []);

  return (
    <div className="flex items-center justify-center">
      <h1 className="text-3xl font-bold">{msg}</h1>
    </div>
  );
}

export default Home;
