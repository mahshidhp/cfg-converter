import React, { Component, Fragment } from "react";
import Converter from "./components/converter";
import Navbar from "./components/navbar";
import About from "./components/about";
import Footer from "./components/footer";
import "./App.css";

class App extends Component {
  state = {
    nightMode: true,
  };

  render() {
    return (
      <Fragment>
        <Navbar
          handleThemeToggle={this.handleThemeToggle}
          nightMode={this.state.nightMode}
        />
        <About />
        <Converter />
        <Footer />
      </Fragment>
    );
  }

  handleThemeToggle = (event) => {
    const { checked } = event.target;
    this.setState({ nightMode: checked });
    const root = document.querySelector(":root");
    if (checked) {
      root.style.setProperty("--bg-color", "#545a5f");
      root.style.setProperty("--border-color", "#37aa9c");
      root.style.setProperty("--accent-color", "#1a1a1b");
      root.style.setProperty("--text-color", "white");
      root.style.setProperty("--highlight-color", "#94f3e4");
      root.style.setProperty("--shadow", 0.1);
    } else {
      root.style.setProperty("--bg-color", "#fff2f2");
      root.style.setProperty("--border-color", "#f47c7c");
      root.style.setProperty("--accent-color", "#fad4d4");
      root.style.setProperty("--text-color", "#4b4b4b");
      root.style.setProperty("--highlight-color", "#4b4b4b");
      root.style.setProperty("--shadow", 0.01);
    }
  };
}

export default App;
