import React, { useState } from "react";
import ModuleList from "./ModuleList";
import EndplateList from "./EndplateList";
import SignalList from "./SignalList";
import SwitchList from "./SwitchList";
import BlockList from "./BlockList";
import DispatcherList from "./DispatcherList";
import TrainList from "./TrainList";
import ConfigPage from "./ConfigPage";
import YardMasterList from "./YardMasterList";

function App() {
  const [apiUrl, setApiUrl] = useState(localStorage.getItem("apiUrl") || "http://localhost:8000");
  const [showConfig, setShowConfig] = useState(false);

  return (
    <div>
      <h1>Free-Dispatcher UI</h1>
      <button onClick={() => setShowConfig(!showConfig)}>
        {showConfig ? "Back to App" : "Configuration"}
      </button>
      {showConfig ? (
        <ConfigPage apiUrl={apiUrl} setApiUrl={setApiUrl} />
      ) : (
        <>
          <ModuleList apiUrl={apiUrl} />
          <EndplateList apiUrl={apiUrl} />
          <SignalList apiUrl={apiUrl} />
          <SwitchList apiUrl={apiUrl} />
          <BlockList apiUrl={apiUrl} />
          <DispatcherList apiUrl={apiUrl} />
          <TrainList apiUrl={apiUrl} />
          <YardMasterList apiUrl={apiUrl} />
        </>
      )}
    </div>
  );
}

export default App;
