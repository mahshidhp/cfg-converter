import React, { Component, Fragment } from "react";

class ProductionRule extends Component {
  state = {};
  render() {
    const lhs = (
      <input
        value={this.props.lhs}
        onKeyDown={(event) =>
          this.props.handleKeyDown(event, this.props.ruleIndex, null)
        }
        onChange={(event) => {
          this.props.handleInputChange(event, this.props.ruleIndex, null);
        }}
      />
    );

    const rhs = this.props.rhs.map((r, rhsIndex) => (
      <Fragment>
        <input
          value={r}
          key={rhsIndex}
          onKeyDown={(event) =>
            this.props.handleKeyDown(event, this.props.ruleIndex, rhsIndex)
          }
          onChange={(event) => {
            this.props.handleInputChange(event, this.props.ruleIndex, rhsIndex);
          }}
        />
        <span className="arrow"> | </span>
      </Fragment>
    ));

    const rhsBtn = (
      <button
        className="add-btn"
        onClick={() => {
          this.props.addRHS(this.props.ruleIndex);
        }}
      >
        +
      </button>
    );

    const arrow = <span className="arrow"> &#8594; </span>;

    return (
      <div className="m-3">
        {lhs}
        {arrow}
        {rhs}
        {rhsBtn}
      </div>
    );
  }
}

export default ProductionRule;
