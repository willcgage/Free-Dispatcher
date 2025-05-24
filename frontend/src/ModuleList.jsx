import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ModuleList({ apiUrl }) {
  const [modules, setModules] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    fetchModules();
  }, [apiUrl]);

  const fetchModules = async () => {
    const res = await axios.get(`${apiUrl}/modules/`);
    setModules(res.data);
  };

  const handleAdd = async () => {
    await axios.post(`${apiUrl}/modules/`, { name, description });
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
