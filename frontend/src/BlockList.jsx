import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

export default function BlockList() {
  const [blocks, setBlocks] = useState([]);
  const [name, setName] = useState("");
  const [startModuleId, setStartModuleId] = useState("");
  const [endModuleId, setEndModuleId] = useState("");

  useEffect(() => {
    fetchBlocks();
  }, []);

  const fetchBlocks = async () => {
    const res = await axios.get(`${API_URL}/blocks/`);
    setBlocks(res.data);
  };

  const handleAdd = async () => {
    await axios.post(`${API_URL}/blocks/`, {
      name,
      start_module_id: startModuleId,
      end_module_id: endModuleId,
    });
    setName("");
    setStartModuleId("");
    setEndModuleId("");
    fetchBlocks();
  };

  return (
    <div>
      <h2>Blocks</h2>
      <ul>
        {blocks.map((b) => (
          <li key={b.id}>
            Name: {b.name}, Start Module: {b.start_module_id}, End Module: {b.end_module_id}
          </li>
        ))}
      </ul>
      <input
        placeholder="Name"
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <input
        placeholder="Start Module ID"
        value={startModuleId}
        onChange={e => setStartModuleId(e.target.value)}
      />
      <input
        placeholder="End Module ID"
        value={endModuleId}
        onChange={e => setEndModuleId(e.target.value)}
      />
      <button onClick={handleAdd}>Add Block</button>
    </div>
  );
}
