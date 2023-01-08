import React, { Component } from "react";

class Result extends Component {
  render() {
    return (
      <div className="row">
        <div className="col card-shadow">
          <div className="row justify-content-center">
            <div className="col-11">
              {this.renderHeader()}
              {this.renderFinalResult()}
              {this.renderSimplificationHistory()}
            </div>
          </div>
        </div>
      </div>
    );
  }

  renderHeader() {
    return (
      <div className="col header">
        <h1 className="highlighted">Result</h1>
        <hr className="highlighted" />
        <ul>
          {this.props.conversionMessages.map((msg, id) => (
            <li key={id}>{msg}</li>
          ))}
        </ul>
      </div>
    );
  }

  renderFinalResult() {
    return (
      <div className="row header">
        <div className="col-6">
          <h5>Original grammar</h5>
          <hr />
          {this.printGrammar(this.props.productionRules)}
        </div>
        <div className="col-6">
          <h5>Converted grammar</h5>
          <hr />
          {this.printGrammar(this.props.resultProductionRules)}
        </div>
      </div>
    );
  }

  renderSimplificationHistory() {
    return (
      <div className="row header">
        <div className="col">
          <h5 className="highlighted">Simplification History</h5>
          <hr className="highlighted" />

          {this.props.simplificationTimeline.map((grammar, id) => (
            <div className="col" key={id}>
              <p>
                <span className="highlighted">Step {id + 1}: </span>
                {this.props.simplificationMessages[id]}
              </p>
              {this.printGrammar(grammar)}
              <hr />
            </div>
          ))}
        </div>
      </div>
    );
  }

  printGrammar(grammar) {
    if (grammar.length > 0) {
      return grammar.map((rule) => <p>{rule.lhs + "  →  " + rule.rhs}</p>);
    }
    return <p className="fst-italic text-secondary">[Empty grammar]</p>;
  }
}

export default Result;
