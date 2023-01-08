import React, { Component, Fragment } from "react";
const arrow = <span className="arrow"> &#8594; </span>;

class ProductionRule extends Component {
  render() {
    const { ruleIndex } = this.props;
    return (
      <div className="m-3">
        {this.renderLHS(ruleIndex)}
        {arrow}
        {this.renderRHS(ruleIndex)}
        {this.renderAddRhsButton(ruleIndex)}
      </div>
    );
  }

  renderLHS(ruleIndex) {
    return (
      <input
        className="lhs-input"
        value={this.props.lhs}
        onKeyDown={(event) => this.props.handleKeyDown(event, ruleIndex, null)}
        onChange={(event) => {
          this.props.handleInputChange(event, ruleIndex, null);
        }}
      />
    );
  }

  renderRHS(ruleIndex) {
    return this.props.rhs.map((r, rhsIndex) => (
      <Fragment key={rhsIndex}>
        <input
          value={r}
          className="rhs-input"
          onKeyDown={(event) =>
            this.props.handleKeyDown(event, ruleIndex, rhsIndex)
          }
          onChange={(event) => {
            this.props.handleInputChange(event, ruleIndex, rhsIndex);
          }}
        />
        <span className="arrow"> | </span>
      </Fragment>
    ));
  }

  renderAddRhsButton(ruleIndex) {
    return (
      <button
        className="add-btn"
        onClick={() => {
          this.props.addRHS(ruleIndex);
        }}
      >
        +
      </button>
    );
  }
}

export default ProductionRule;
