import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000"; // Change if deploying

export default function ModuleList() {
  const [modules, setModules] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    fetchModules();
  }, []);

  const fetchModules = async () => {
    const res = await axios.get(`${API_URL}/modules/`);
    setModules(res.data);
  };

  const handleAdd = async () => {
    await axios.post(`${API_URL}/modules/`, { name, description });
    setName("");
    setDescription("");
    fetchModules();
  };

  return (
    <div>
      <h2>Modules</h2>
      <ul>
        {modules.map((m) => (
          <li key={m.id}>{m.name} - {m.description}</li>
        ))}
      </ul>
      <input
        placeholder="Module name"
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <input
        placeholder="Description"
        value={description}
        onChange={e => setDescription(e.target.value)}
      />
      <button onClick={handleAdd}>Add Module</button>
    </div>
  );
}
