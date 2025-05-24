import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

export default function EndplateList() {
  const [endplates, setEndplates] = useState([]);
  const [moduleId, setModuleId] = useState("");
  const [position, setPosition] = useState("");
  const [isBlockEnd, setIsBlockEnd] = useState(false);

  useEffect(() => {
    fetchEndplates();
  }, []);

  const fetchEndplates = async () => {
    const res = await axios.get(`${API_URL}/endplates/`);
    setEndplates(res.data);
  };

  const handleAdd = async () => {
    await axios.post(`${API_URL}/endplates/`, {
      module_id: moduleId,
      position: Number(position),
      is_block_end: isBlockEnd,
    });
    setModuleId("");
    setPosition("");
    setIsBlockEnd(false);
    fetchEndplates();
  };

  return (
    <div>
      <h2>Endplates</h2>
      <ul>
        {endplates.map((e) => (
          <li key={e.id}>
            Module: {e.module_id}, Position: {e.position}, Block End: {e.is_block_end ? "Yes" : "No"}
          </li>
        ))}
      </ul>
      <input
        placeholder="Module ID"
        value={moduleId}
        onChange={e => setModuleId(e.target.value)}
      />
      <input
        placeholder="Position"
        type="number"
        value={position}
        onChange={e => setPosition(e.target.value)}
      />
      <label>
        Block End
        <input
          type="checkbox"
          checked={isBlockEnd}
          onChange={e => setIsBlockEnd(e.target.checked)}
        />
      </label>
      <button onClick={handleAdd}>Add Endplate</button>
    </div>
  );
}
