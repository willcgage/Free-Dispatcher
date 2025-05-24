import React, { useEffect, useState } from "react";
import axios from "axios";

export default function TrainList({ apiUrl }) {
  const [trains, setTrains] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [dispatcherId, setDispatcherId] = useState("");
  const [blockId, setBlockId] = useState("");

  useEffect(() => {
    fetchTrains();
  }, [apiUrl]);

  const fetchTrains = async () => {
    const res = await axios.get(`${apiUrl}/trains/`);
    setTrains(res.data);
  };

  const handleAdd = async () => {
    await axios.post(`${apiUrl}/trains/`, {
      name,
      description,
      dispatcher_id: dispatcherId || null,
      block_id: blockId || null,
    });
    setName("");
    setDescription("");
    setDispatcherId("");
    setBlockId("");
    fetchTrains();
  };

  return (
    <div>
      <h2>Trains</h2>
      <ul>
        {trains.map((t) => (
          <li key={t.id}>
            {t.name}
            {t.description && ` - ${t.description}`}
            {t.dispatcher_id && ` (Dispatcher: ${t.dispatcher_id})`}
            {t.block_id && ` (Block: ${t.block_id})`}
          </li>
        ))}
      </ul>
      <input
        placeholder="Name"
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <input
        placeholder="Description"
        value={description}
        onChange={e => setDescription(e.target.value)}
      />
      <input
        placeholder="Dispatcher ID (optional)"
        value={dispatcherId}
        onChange={e => setDispatcherId(e.target.value)}
      />
      <input
        placeholder="Block ID (optional)"
        value={blockId}
        onChange={e => setBlockId(e.target.value)}
      />
      <button onClick={handleAdd}>Add Train</button>
    </div>
  );
}
