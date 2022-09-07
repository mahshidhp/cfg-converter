import React, { Component } from "react";

class SelectCFG extends Component {
  render() {
    return (
      <div id="selectForm">
        <select
          className="form-select"
          style={{ width: "100%" }}
          onChange={(e) => {
            this.props.handleSelectForm(e);
          }}
        >
          <option selected>select CFG Form</option>
          <option value="1">Chomsky Normal Form (CNF)</option>
          <option value="2">Greibach Normal Form (GNF)</option>
        </select>
      </div>
    );
  }
}

export default SelectCFG;
