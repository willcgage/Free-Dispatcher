import React, { useEffect, useState } from "react";
import axios from "axios";

export default function DispatcherList({ apiUrl }) {
  const [dispatchers, setDispatchers] = useState([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    fetchDispatchers();
  }, [apiUrl]);

  const fetchDispatchers = async () => {
    const res = await axios.get(`${apiUrl}/dispatchers/`);
    setDispatchers(res.data);
  };

  const handleAdd = async () => {
    await axios.post(`${apiUrl}/dispatchers/`, { name, email });
    setName("");
    setEmail("");
    fetchDispatchers();
  };

  return (
    <div>
      <h2>Dispatchers</h2>
      <ul>
        {dispatchers.map((d) => (
          <li key={d.id}>{d.name} {d.email && `(${d.email})`}</li>
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
      <button onClick={handleAdd}>Add Dispatcher</button>
    </div>
  );
}
