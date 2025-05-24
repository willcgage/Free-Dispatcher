import React from "react";
import ModuleList from "./ModuleList";
import EndplateList from "./EndplateList";
import SignalList from "./SignalList";
import SwitchList from "./SwitchList";
import BlockList from "./BlockList";

function App() {
  return (
    <div>
      <h1>Free-Dispatcher UI</h1>
      <ModuleList />
      <EndplateList />
      <SignalList />
      <SwitchList />
      <BlockList />
    </div>
  );
}

export default App;
