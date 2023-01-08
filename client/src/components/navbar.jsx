import React, { Component } from "react";

class Navbar extends Component {
  render() {
    return (
      <nav
        className={this.getNavbarClasses()}
        aria-label="Third navbar example"
      >
        <div className="container-fluid">
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarsExample03"
            aria-controls="navbarsExample03"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse" id="navbarsExample03">
            <ul className="navbar-nav me-auto mb-2 mb-sm-0">
              <li className="nav-item">
                <a
                  className="nav-link active mx-2"
                  href="https://github.com/mahshidhp/cfg-converter"
                  target={"_blank"}
                >
                  {this.renderGithubIcon()}
                  Github
                </a>
              </li>
            </ul>
          </div>
          {/* dark/light mode toggle */}
          <div className="form-check form-switch form-check-reverse">
            {this.renderNightModeIcon()}
            <input
              className="form-check-input mx-2"
              type="checkbox"
              role="switch"
              defaultChecked
              onChange={(event) => this.props.handleThemeToggle(event)}
            />
          </div>
        </div>
      </nav>
    );
  }

  getNavbarClasses() {
    let classes = "navbar navbar-expand-sm ";
    if (this.props.nightMode) {
      classes += "navbar-dark bg-dark";
    } else {
      classes += "navbar-light bg-light";
    }
    return classes;
  }

  renderGithubIcon() {
    return (
      <svg width="30px" height="30px" viewBox="0 0 32 32">
        <path
          d="M16 1.375c-8.282 0-14.996 6.714-14.996 14.996 0 6.585 4.245 12.18 10.148 14.195l0.106 0.031c0.75 0.141 1.025-0.322 1.025-0.721 0-0.356-0.012-1.3-0.019-2.549-4.171 0.905-5.051-2.012-5.051-2.012-0.288-0.925-0.878-1.685-1.653-2.184l-0.016-0.009c-1.358-0.93 0.105-0.911 0.105-0.911 0.987 0.139 1.814 0.718 2.289 1.53l0.008 0.015c0.554 0.995 1.6 1.657 2.801 1.657 0.576 0 1.116-0.152 1.582-0.419l-0.016 0.008c0.072-0.791 0.421-1.489 0.949-2.005l0.001-0.001c-3.33-0.375-6.831-1.665-6.831-7.41-0-0.027-0.001-0.058-0.001-0.089 0-1.521 0.587-2.905 1.547-3.938l-0.003 0.004c-0.203-0.542-0.321-1.168-0.321-1.821 0-0.777 0.166-1.516 0.465-2.182l-0.014 0.034s1.256-0.402 4.124 1.537c1.124-0.321 2.415-0.506 3.749-0.506s2.625 0.185 3.849 0.53l-0.1-0.024c2.849-1.939 4.105-1.537 4.105-1.537 0.285 0.642 0.451 1.39 0.451 2.177 0 0.642-0.11 1.258-0.313 1.83l0.012-0.038c0.953 1.032 1.538 2.416 1.538 3.937 0 0.031-0 0.061-0.001 0.091l0-0.005c0 5.761-3.505 7.029-6.842 7.398 0.632 0.647 1.022 1.532 1.022 2.509 0 0.093-0.004 0.186-0.011 0.278l0.001-0.012c0 2.007-0.019 3.619-0.019 4.106 0 0.394 0.262 0.862 1.031 0.712 6.028-2.029 10.292-7.629 10.292-14.226 0-8.272-6.706-14.977-14.977-14.977-0.006 0-0.013 0-0.019 0h0.001z"
          style={{ fill: this.props.nightMode ? "#FFFFFF" : "#000000" }}
        ></path>
      </svg>
    );
  }

  renderNightModeIcon() {
    return (
      <svg width="30px" height="30px" viewBox="0 0 24 24">
        <path
          d="M12,2h-.46a1,1,0,0,0-.44,1.86A5.94,5.94,0,0,1,14,9,6,6,0,0,1,3.93,13.4a1,1,0,0,0-1.65,1A10,10,0,1,0,12,2Z"
          style={{ fill: this.props.nightMode ? "#0d6efd" : "#cccccc" }}
        ></path>
      </svg>
    );
  }
}

export default Navbar;
