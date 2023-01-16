import React, { Component, Fragment } from "react";
import ProductionRule from "./productionRule";
import SelectCFG from "./selectCFG";
import exampleGrammars from "../sampleGrammars.json";

class InputGrammar extends Component {
  render() {
    return (
      <div className="col-lg card-shadow">
        {this.renderDescription()}
        <SelectCFG handleSelectForm={this.props.handleSelectForm} />
        {this.renderProductionRules()}
        {this.renderButtons()}
        {this.renderErrorMessage()}
      </div>
    );
  }

  renderErrorMessage() {
    const { errorMessage } = this.props;
    return (
      errorMessage && (
        <div className="error-msg">
          {failIcon}
          <span className="fw-bold">Error: </span>
          {errorMessage}
        </div>
      )
    );
  }

  renderProductionRules() {
    const productionRules = this.props.productionRules.map(
      (productionRule, ruleIndex) => (
        <ProductionRule
          lhs={productionRule.lhs}
          rhs={productionRule.rhs}
          handleKeyDown={this.props.handleKeyDown}
          handleInputChange={this.props.handleInputChange}
          handleRuleDeletion={this.props.handleRuleDeletion}
          addRHS={this.props.addRHS}
          ruleIndex={ruleIndex}
          key={ruleIndex}
        />
      )
    );
    return productionRules;
  }

  renderDescription() {
    const terminals = " ! * + - / , ; : \" ' ( ) { } < > [ ] \\ # ";
    return (
      <div className="text-start header">
        <h1 className="highlighted">CFG</h1>
        <p className="highlighted">
          Enter your context-free grammar (CFG) and select normal form to
          convert.
        </p>
        <p>
          - Use "S" as start symbol.
          <br />
          - Use upper-case letters as non-terminals.
          <br />- Use lower-case letters, numbers and
          <span className="highlighted">{terminals}</span>
          as terminals.
        </p>
        <p>You can use these example grammars:</p>
        {this.renderExampleGrammarButtons()}
        <hr className="highlighted" />
      </div>
    );
  }

  renderExampleGrammarButtons() {
    return (
      <Fragment>
        {exampleGrammars.map((example, i) => (
          <button
            key={i}
            className="btn-sm example-btn"
            onClick={() => this.props.handleExampleInputLoad(i)}
          >
            Example {i + 1}
          </button>
        ))}
      </Fragment>
    );
  }

  renderButtons() {
    return (
      <div className="text-center">
        <button
          className="m-2 transparent-button"
          onClick={this.props.addProductionRule}
        >
          Add production rule
        </button>
        <button className="m-2 transparent-button" onClick={this.props.reset}>
          Reset
        </button>
        <br />
        <a href="#result">
          <button
            className="btn-lg m-2 main-button"
            onClick={this.props.convert}
          >
            Convert
          </button>
        </a>
      </div>
    );
  }
}

const failIcon = (
  <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z" />
  </svg>
);

export default InputGrammar;
