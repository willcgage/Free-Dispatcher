import React, { useEffect, useState } from "react";
import axios from "axios";

export default function TrainList({ apiUrl }) {
  const [trains, setTrains] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [dispatcherId, setDispatcherId] = useState("");

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
    });
    setName("");
    setDescription("");
    setDispatcherId("");
    fetchTrains();
  };

  return (
    <div>
      <h2>Trains</h2>
      <ul>
        {trains.map((t) => (
          <li key={t.id}>
            {t.name} {t.description && `- ${t.description}`} {t.dispatcher_id && `(Dispatcher: ${t.dispatcher_id})`}
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
      <button onClick={handleAdd}>Add Train</button>
    </div>
  );
}
