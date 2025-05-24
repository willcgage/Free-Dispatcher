import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

export default function SwitchList() {
  const [switches, setSwitches] = useState([]);
  const [moduleId, setModuleId] = useState("");
  const [name, setName] = useState("");
  const [type, setType] = useState("");

  useEffect(() => {
    fetchSwitches();
  }, []);

  const fetchSwitches = async () => {
    const res = await axios.get(`${API_URL}/switches/`);
    setSwitches(res.data);
  };

  const handleAdd = async () => {
    await axios.post(`${API_URL}/switches/`, {
      module_id: moduleId,
      name,
      type,
    });
    setModuleId("");
    setName("");
    setType("");
    fetchSwitches();
  };

  return (
    <div>
      <h2>Switches</h2>
      <ul>
        {switches.map((s) => (
          <li key={s.id}>
            Module: {s.module_id}, Name: {s.name}, Type: {s.type}
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
        placeholder="Type"
        value={type}
        onChange={e => setType(e.target.value)}
      />
      <button onClick={handleAdd}>Add Switch</button>
    </div>
  );
}
