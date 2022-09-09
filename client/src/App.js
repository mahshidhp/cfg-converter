import React, { Component } from "react";
import Converter from "./components/converter";
import Navbar from "./components/navbar";
import About from "./components/about";

import "./App.css";

class App extends Component {
  state = {};
  render() {
    return (
      <div>
        <Navbar />
        <Converter />
        <About />
      </div>
    );
  }
}

export default App;
