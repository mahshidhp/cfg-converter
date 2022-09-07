import React, { Component } from "react";
import Converter from "./components/converter";
import Navbar from "./components/navbar";

import "./App.css";

class App extends Component {
  state = {};
  render() {
    return (
      <div>
        <Navbar />
        <Converter />
      </div>
    );
  }
}

export default App;
