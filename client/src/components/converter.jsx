import React, { Component } from "react";
import InputGrammar from "./inputGrammar";
import Test from "./test";
import Result from "./result";

const EPSILON = String.fromCharCode(949);

class Converter extends Component {
  constructor() {
    super();
    //bind "this" for component methods
    this.reset = this.reset.bind(this);
    this.addRHS = this.addRHS.bind(this);
    this.addProductionRule = this.addProductionRule.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.handleSelectForm = this.handleSelectForm.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.convert = this.convert.bind(this);
    this.test = this.test.bind(this);
    this.postData = this.postData.bind(this);

    this.state = {
      productionRules: [],
      resultProductionRules: [],
      conversionForm: null,
      conversionMessages: [],

      //test-component
      isDerivedFromOriginalGrammar: null,
      isDerivedFromResultGrammar: null,
    };
  }

  render() {
    return (
      <div className="container text-center m-4">
        <InputGrammar
          productionRules={this.state.productionRules}
          reset={this.reset}
          addProductionRule={this.addProductionRule}
          addRHS={this.addRHS}
          handleKeyDown={this.handleKeyDown}
          handleSelectForm={this.handleSelectForm}
          handleInputChange={this.handleInputChange}
          convert={this.convert}
        />
        <Result
          productionRules={this.state.productionRules}
          resultProductionRules={this.state.resultProductionRules}
          conversionMessages={this.state.conversionMessages}
        />
        <Test
          test={this.test}
          isDerivedFromOriginalGrammar={this.state.isDerivedFromOriginalGrammar}
          isDerivedFromResultGrammar={this.state.isDerivedFromResultGrammar}
        />
      </div>
    );
  }

  reset() {
    this.setState({
      productionRules: [],
      resultProductionRules: [],
      conversionMessages: [],
      isDerivedFromOriginalGrammar: null,
      isDerivedFromResultGrammar: null,
    });
  }

  addRHS(ruleId) {
    const productionRules = this.state.productionRules;
    productionRules[ruleId].rhs.push(EPSILON);
    this.setState({ productionRules });
  }

  addProductionRule() {
    let productionRules = this.state.productionRules;
    const newRule =
      productionRules.length === 0
        ? { lhs: "S", rhs: [EPSILON] }
        : { lhs: null, rhs: [EPSILON] };
    productionRules = productionRules.concat(newRule);
    this.setState({ productionRules });
  }

  handleSelectForm(e) {
    this.setState({ conversionForm: e.target.value });
  }

  handleInputChange(event, ruleId, rhsId) {
    const productionRules = this.state.productionRules;
    if (rhsId == null) {
      productionRules[ruleId].lhs = event.target.value;
    } else {
      productionRules[ruleId].rhs[rhsId] = event.target.value;
    }
    this.setState({ productionRules });
  }

  handleKeyDown(e, ruleId, rhsId) {
    if (e.key === "|") {
      e.preventDefault();
      if (rhsId != null) {
        this.addRHS(ruleId);
      }
    } else if (e.key === "Enter") {
      e.preventDefault();
      this.addProductionRule();
    }
  }

  convert() {
    const requestData = {
      grammar: this.state.productionRules,
      conversionForm: this.state.conversionForm,
    };
    this.postData("/convert", requestData).then((data) => {
      console.log("conversion response", data);
      this.setState({
        resultProductionRules: data.convertedGrammar,
        conversionMessages: data.conversionMessages,
      });
    });
  }

  test(string) {
    const requestData = {
      grammar: this.state.productionRules,
      resultGrammar: this.state.resultProductionRules,
      string: string,
    };

    this.postData("/test", requestData).then((data) => {
      console.log("test response", data);
      this.setState({
        isDerivedFromOriginalGrammar: data.isDerivedFromOriginalGrammar,
        isDerivedFromResultGrammar: data.isDerivedFromResultGrammar,
      });
    });
  }

  async postData(url, data) {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    return response.json();
  }
}

export default Converter;
