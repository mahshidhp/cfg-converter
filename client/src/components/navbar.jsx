import React, { Component } from "react";

class Navbar extends Component {
  state = {};
  render() {
    return (
      <nav
        className="navbar navbar-expand-md navbar-dark bg-dark"
        aria-label="Fourth navbar example"
      >
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            CFG Converter
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarsExample04"
            aria-controls="navbarsExample04"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse">
            <ul className="navbar-nav me-auto mb-2 mb-md-0">
              <li className="nav-item">
                <a className="nav-link active" href="/about">
                  About
                </a>
              </li>
              <li className="nav-item">
                <a
                  className="nav-link active"
                  href="https://github.com/mahshidhp/cfg-converter"
                  target={"_blank"}
                >
                  Github
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    );
  }
}

export default Navbar;
