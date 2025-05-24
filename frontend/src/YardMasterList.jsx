import React, { useEffect, useState } from "react";
import axios from "axios";

export default function YardMasterList({ apiUrl }) {
  const [yardmasters, setYardmasters] = useState([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    fetchYardmasters();
  }, [apiUrl]);

  const fetchYardmasters = async () => {
    const res = await axios.get(`${apiUrl}/yardmasters/`);
    setYardmasters(res.data);
  };

  const handleAdd = async () => {
    await axios.post(`${apiUrl}/yardmasters/`, { name, email });
    setName("");
    setEmail("");
    fetchYardmasters();
  };

  return (
    <div>
      <h2>YardMasters</h2>
      <ul>
        {yardmasters.map((y) => (
          <li key={y.id}>{y.name} {y.email && `(${y.email})`}</li>
        ))}
      </ul>
      <input
        placeholder="Name"
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <input
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      />
      <button onClick={handleAdd}>Add YardMaster</button>
    </div>
  );
}
