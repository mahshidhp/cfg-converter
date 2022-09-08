import React, { Component } from "react";

class Result extends Component {
  printGrammar(grammar) {
    return grammar.map((rule) => <p>{rule.lhs + "  →  " + rule.rhs}</p>);
  }

  render() {
    return (
      <div className="row text-start">
        <div className="card-shadow">
          <div className="col-md-12 light-text">
            <h1>Result</h1>
            <hr />
            <ul>
              {this.props.conversionMessages.map((msg, id) => (
                <li key={id}>{msg}</li>
              ))}
            </ul>
          </div>
          <div className="row" style={{ padding: "0px 30px" }}>
            <div className="col-md-6 light-text">
              <h5>Original grammar</h5>
              <hr />
              {this.printGrammar(this.props.productionRules)}
            </div>
            <div className="col-md-6 light-text">
              <h5>Converted grammar</h5>
              <hr />
              {this.printGrammar(this.props.resultProductionRules)}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Result;
