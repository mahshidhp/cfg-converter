import React, { Component } from "react";

class TestCase extends Component {
  render() {
    return (
      <div className="row">
        <div className="col card-shadow">
          <div className="row justify-content-center">
            <div className="col-11">
              {this.renderHeader()}
              {this.renderTestCases()}
            </div>
          </div>
        </div>
      </div>
    );
  }

  renderHeader() {
    return (
      <div className="col header">
        <h1 className="highlighted" id="result">
          Testcases
        </h1>
        <hr className="highlighted" />
        <button
          className="btn-lg main-button"
          onClick={this.props.generateTestCases}
        >
          Generate
        </button>
      </div>
    );
  }

  renderTestCases() {
    return (
      <div className="row header">
        <div className="col-sm-6 ">
          <h5 className="success-text">Accepted by original grammar</h5>
          <hr className="success-text" />
          <ul>
            {this.props.acceptedByOriginalGrammar.map((word, index) => (
              <li key={index}>{word}</li>
            ))}
          </ul>
        </div>
        <div className="col-sm-6">
          <h5 className="success-text">Accepted by converted grammar</h5>
          <hr className="success-text" />
          <ul>
            {this.props.acceptedByConvertedGrammar.map((word, index) => (
              <li key={index}>{word}</li>
            ))}
          </ul>
        </div>

        <div className="col-sm-6">
          <h5 className="fail-text">Rejected by original grammar</h5>
          <hr className="fail-text" />
          <ul>
            {this.props.rejectedByOriginalGrammar.map((word, index) => (
              <li key={index}>{word}</li>
            ))}
          </ul>
        </div>
        <div className="col-sm-6">
          <h5 className="fail-text">Rejected by converted grammar</h5>
          <hr className="fail-text" />
          <ul>
            {this.props.rejectedByConvertedGrammar.map((word, index) => (
              <li key={index}>{word}</li>
            ))}
          </ul>
        </div>
      </div>
    );
  }
}

export default TestCase;
