import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

export default function SignalList() {
  const [signals, setSignals] = useState([]);
  const [moduleId, setModuleId] = useState("");
  const [name, setName] = useState("");
  const [position, setPosition] = useState("");

  useEffect(() => {
    fetchSignals();
  }, []);

  const fetchSignals = async () => {
    const res = await axios.get(`${API_URL}/signals/`);
    setSignals(res.data);
  };

  const handleAdd = async () => {
    await axios.post(`${API_URL}/signals/`, {
      module_id: moduleId,
      name,
      position,
    });
    setModuleId("");
    setName("");
    setPosition("");
    fetchSignals();
  };

  return (
    <div>
      <h2>Signals</h2>
      <ul>
        {signals.map((s) => (
          <li key={s.id}>
            Module: {s.module_id}, Name: {s.name}, Position: {s.position}
          </li>
        ))}
      </ul>
      <input
        placeholder="Module ID"
        value={moduleId}
        onChange={e => setModuleId(e.target.value)}
      />
      <input
        placeholder="Name"
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <input
        placeholder="Position"
        value={position}
        onChange={e => setPosition(e.target.value)}
      />
      <button onClick={handleAdd}>Add Signal</button>
    </div>
  );
}
