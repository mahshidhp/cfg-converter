import React, { Component } from "react";

class Test extends Component {
  render() {
    return (
      <div className="col-lg card-shadow text-start">
        {this.renderDescription()}
        {this.renderInput()}
        {this.renderResult()}
      </div>
    );
  }

  renderDescription() {
    return (
      <div className="header">
        <h1 className="highlighted">Test</h1>
        <p className="highlighted">
          Enter a string to check if it is derived from the original and result
          grammars
        </p>
        <hr className="highlighted" />
      </div>
    );
  }

  renderInput() {
    return (
      <div className="text-center">
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
  }

  renderResult() {
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
      <div className="header">
        <p>Original grammar:</p>
        {this.props.isDerivedFromOriginalGrammar ? success : fail}
        <p>Result grammar:</p>
        {this.props.isDerivedFromResultGrammar ? success : fail}
      </div>
    );
    return result;
  }
}

const successIcon = (
  <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z" />
  </svg>
);
const failIcon = (
  <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z" />
  </svg>
);

export default Test;
