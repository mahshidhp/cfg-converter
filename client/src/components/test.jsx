import React, { Component } from "react";

class Test extends Component {
  render() {
    const description = (
      <div className="light-text">
        <h1>Test</h1>
        <p>
          Enter a string to check it is derived by the original and result
          grammar
        </p>
        <hr />
      </div>
    );
    const input = (
      <div>
        <input type="text" onChange={this.props.handleTestStringChange} />
        <button
          type="submit"
          className="main-button m-2"
          onClick={this.props.test}
        >
          Check!
        </button>
      </div>
    );
    const success = (
      <div className="m-2 test-result test-success">
        {successIcon}
        Derives from grammar!
      </div>
    );
    const fail = (
      <div className="m-2 test-result test-fail">
        {failIcon}
        Does not derive from grammar!
      </div>
    );
    const result = (
      <div className="light-text">
        <p>Original grammar:</p>
        {this.props.isDerivedFromOriginalGrammar ? success : fail}
        <p>Result grammar:</p>
        {this.props.isDerivedFromResultGrammar ? success : fail}
      </div>
    );

    return (
      <div className="row">
        <div className="col-md-2"></div>
        <div className="col-md-8 card-shadow">
          {description}
          {input}
          {result}
        </div>
        <div className="col-md-2"></div>
      </div>
    );
  }
}

const successIcon = (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="16"
    height="16"
    fill="currentColor"
    className="bi bi-check-circle-fill"
    viewBox="0 0 16 16"
  >
    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z" />
  </svg>
);
const failIcon = (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="16"
    height="16"
    fill="currentColor"
    className="bi bi-exclamation-circle-fill"
    viewBox="0 0 16 16"
  >
    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z" />
  </svg>
);
export default Test;
