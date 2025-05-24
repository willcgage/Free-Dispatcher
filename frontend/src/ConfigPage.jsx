import React, { useState, useEffect } from "react";

export default function ConfigPage({ apiUrl, setApiUrl }) {
  const [input, setInput] = useState(apiUrl);

  useEffect(() => {
    setInput(apiUrl);
  }, [apiUrl]);

  const handleSave = () => {
    setApiUrl(input);
    localStorage.setItem("apiUrl", input);
    alert("API URL saved!");
  };

  return (
    <div>
      <h2>Configuration</h2>
      <label>
        API Base URL:
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="http://localhost:8000"
        />
      </label>
      <button onClick={handleSave}>Save</button>
    </div>
  );
}
