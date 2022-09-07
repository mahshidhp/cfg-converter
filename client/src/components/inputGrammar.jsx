import React, { Component, Fragment } from "react";
import ProductionRule from "./productionRule";
import SelectCFG from "./selectCFG";

class InputGrammar extends Component {
  render() {
    const productionRules = this.props.productionRules.map(
      (productionRule, ruleIndex) => (
        <ProductionRule
          lhs={productionRule.lhs}
          rhs={productionRule.rhs}
          handleKeyDown={this.props.handleKeyDown}
          handleInputChange={this.props.handleInputChange}
          addRHS={this.props.addRHS}
          ruleIndex={ruleIndex}
          key={ruleIndex}
        />
      )
    );

    return (
      <div className="row">
        <div className="col-md-12 card-shadow">
          {this.renderDescription()}
          <SelectCFG handleSelectForm={this.props.handleSelectForm} />
          {productionRules}
          {this.renderButtons()}
        </div>
      </div>
    );
  }

  renderDescription() {
    return (
      <div className="text-start light-text">
        <h1>CFG</h1>
        <p>
          Enter your context free grammar (CFG) and select normal form to
          convert.
          <br />
          Use "S" as start symbol.
        </p>
        <hr />
      </div>
    );
  }

  renderButtons() {
    return (
      <Fragment>
        <br />
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
        <button className="btn-lg m-2 main-button" onClick={this.props.convert}>
          Convert
        </button>
      </Fragment>
    );
  }
}

export default InputGrammar;
