import React, { Component } from "react";
import InputGrammar from "./inputGrammar";
import Test from "./test";
import Result from "./result";
import TestCase from "./testCase";
import exampleGrammars from "../sampleGrammars.json";

const EPSILON = String.fromCharCode(949);

class Converter extends Component {
  constructor() {
    super();
    this.state = {
      productionRules: [],
      resultProductionRules: [],
      conversionForm: null,
      conversionMessages: [],
      simplificationTimeline: [],
      simplificationMessages: [],
      errorMessage: "",

      //test-component
      testString: "",
      isDerivedFromOriginalGrammar: null,
      isDerivedFromResultGrammar: null,

      //examples
      originalGrammarExamples: [],
      resultGrammarExamples: [],

      //test-cases
      acceptedByOriginalGrammar: [],
      rejectedByOriginalGrammar: [],
      acceptedByConvertedGrammar: [],
      rejectedByConvertedGrammar: [],
    };
  }

  render() {
    return (
      <div className="container">
        <div className="row justify-content-center">
          <InputGrammar
            productionRules={this.state.productionRules}
            reset={this.reset}
            addProductionRule={this.addProductionRule}
            addRHS={this.addRHS}
            handleRuleDeletion={this.handleRuleDeletion}
            handleKeyDown={this.handleKeyDown}
            handleSelectForm={this.handleSelectForm}
            handleInputChange={this.handleInputChange}
            handleExampleInputLoad={this.handleExampleInputLoad}
            convert={this.convert}
            errorMessage={this.state.errorMessage}
          />
          <Test
            test={this.test}
            handleTestStringChange={this.handleTestStringChange}
            isDerivedFromOriginalGrammar={
              this.state.isDerivedFromOriginalGrammar
            }
            isDerivedFromResultGrammar={this.state.isDerivedFromResultGrammar}
          />
        </div>
        <Result
          productionRules={this.state.productionRules}
          resultProductionRules={this.state.resultProductionRules}
          simplificationTimeline={this.state.simplificationTimeline}
          simplificationMessages={this.state.simplificationMessages}
          originalGrammarExamples={this.state.originalGrammarExamples}
          resultGrammarExamples={this.state.resultGrammarExamples}
        />
        <TestCase
          generateTestCases={this.generateTestCases}
          acceptedByOriginalGrammar={this.state.acceptedByOriginalGrammar}
          rejectedByOriginalGrammar={this.state.rejectedByOriginalGrammar}
          acceptedByConvertedGrammar={this.state.acceptedByConvertedGrammar}
          rejectedByConvertedGrammar={this.state.rejectedByConvertedGrammar}
        />
      </div>
    );
  }

  reset = () => {
    this.setState({
      productionRules: [],
      resultProductionRules: [],
      testString: "",
      isDerivedFromOriginalGrammar: null,
      isDerivedFromResultGrammar: null,
      simplificationTimeline: [],
      simplificationMessages: [],
      errorMessage: "",
      originalGrammarExamples: [],
      resultGrammarExamples: [],
      acceptedByOriginalGrammar: [],
      rejectedByOriginalGrammar: [],
      acceptedByConvertedGrammar: [],
      rejectedByConvertedGrammar: [],
    });
  };

  addRHS = (ruleId) => {
    const productionRules = this.state.productionRules;
    productionRules[ruleId].rhs.push(EPSILON);
    this.setState({ productionRules }, () =>
      this.changeFocusToCurrentRHS(ruleId)
    );
  };

  changeFocusToCurrentRHS = (ruleId) => {
    const rhsInputElements = document.getElementsByClassName("rhs-input");
    let rhsId = 0;
    for (let i = 0; i <= ruleId; i++) {
      rhsId += this.state.productionRules[i].rhs.length;
    }
    const currentRHS = rhsInputElements[rhsId - 1];
    currentRHS.focus();
  };

  deleteRHS = (ruleId, rhsId) => {
    const { productionRules } = this.state;
    const newRHS = [...productionRules[ruleId].rhs];
    newRHS.splice(rhsId, 1);
    const newRule = { lhs: productionRules[ruleId].lhs, rhs: newRHS };
    const newRules = productionRules.map((rule, id) =>
      id === ruleId ? newRule : rule
    );
    this.setState({ productionRules: newRules });
  };

  addProductionRule = () => {
    let productionRules = this.state.productionRules;
    const newRule =
      productionRules.length === 0
        ? { lhs: "S", rhs: [EPSILON] }
        : { lhs: "", rhs: [EPSILON] };
    productionRules = productionRules.concat(newRule);
    this.setState({ productionRules }, () => this.changeFocusToLastLHS());
  };

  changeFocusToLastLHS = () => {
    const lhsInputElements = document.getElementsByClassName("lhs-input");
    const lastLhs = lhsInputElements[lhsInputElements.length - 1];
    lastLhs.focus();
  };

  handleRuleDeletion = (ruleId) => {
    const { productionRules } = this.state;
    const newRules = productionRules
      .slice(0, ruleId)
      .concat(productionRules.slice(ruleId + 1));
    this.setState({ productionRules: newRules });
  };

  handleSelectForm = (e) => {
    this.setState({ conversionForm: e.target.value });
  };

  handleInputChange = (event, ruleId, rhsId) => {
    const productionRules = this.state.productionRules;
    const isLHS = rhsId == null;
    const { value: inputValue } = event.target;
    if (isLHS && inputValue.length < 2) {
      productionRules[ruleId].lhs = inputValue;
    } else {
      productionRules[ruleId].rhs[rhsId] = inputValue;
    }
    this.setState({ productionRules });
  };

  handleKeyDown = (e, ruleId, rhsId) => {
    if (e.key === "|") {
      e.preventDefault();
      if (rhsId != null) {
        this.addRHS(ruleId);
      }
    } else if (e.key === "Enter") {
      e.preventDefault();
      this.addProductionRule();
    } else if (e.key === "Backspace") {
      if (
        rhsId !== null &&
        this.state.productionRules[ruleId].rhs[rhsId] === ""
      ) {
        e.preventDefault();
        this.deleteRHS(ruleId, rhsId);
      }
    }
  };

  handleExampleInputLoad = (exampleId) => {
    const exampleRules = JSON.parse(JSON.stringify(exampleGrammars[exampleId])); //deep copy
    this.reset();
    this.setState({ productionRules: exampleRules });
  };

  handleTestStringChange = (event) => {
    this.setState({ testString: event.target.value });
  };

  convert = () => {
    this.setState(
      {
        resultProductionRules: [],
        testString: "",
        isDerivedFromOriginalGrammar: null,
        isDerivedFromResultGrammar: null,
        simplificationTimeline: [],
        simplificationMessages: [],
        errorMessage: "",
        originalGrammarExamples: [],
        resultGrammarExamples: [],
        acceptedByOriginalGrammar: [],
        rejectedByOriginalGrammar: [],
        acceptedByConvertedGrammar: [],
        rejectedByConvertedGrammar: [],
      },
      () => this.convert_()
    );
  };

  convert_ = () => {
    const requestData = {
      grammar: this.state.productionRules,
      conversionForm: this.state.conversionForm,
    };
    this.postData("/convert", requestData).then((data) => {
      this.setState(
        {
          resultProductionRules: data.convertedGrammar,
          simplificationTimeline: data.simplificationTimeline,
          simplificationMessages: data.simplificationMessages,
          errorMessage: data.errorMessage,
        },
        () => this.getExampleWords()
      );
    });
  };

  test = () => {
    const requestData = {
      grammar: this.state.productionRules,
      resultGrammar: this.state.resultProductionRules,
      string: this.state.testString,
    };

    this.postData("/test", requestData).then((data) => {
      this.setState({
        isDerivedFromOriginalGrammar: data.isDerivedFromOriginalGrammar,
        isDerivedFromResultGrammar: data.isDerivedFromResultGrammar,
      });
    });
  };

  getExampleWords = () => {
    const requestData = {
      grammar: this.state.productionRules,
      resultGrammar: this.state.resultProductionRules,
      count: 10,
    };

    this.postData("/examples", requestData).then((data) => {
      this.setState({
        originalGrammarExamples: data.originalGrammarExamples,
        resultGrammarExamples: data.resultGrammarExamples,
      });
    });
  };

  generateTestCases = () => {
    const requestData = {
      grammar: this.state.productionRules,
      resultGrammar: this.state.resultProductionRules,
      count: 10,
    };

    this.postData("/testcase", requestData).then((data) => {
      this.setState({
        acceptedByOriginalGrammar: data.acceptedByOriginalGrammar,
        rejectedByOriginalGrammar: data.rejectedByOriginalGrammar,
        acceptedByConvertedGrammar: data.acceptedByConvertedGrammar,
        rejectedByConvertedGrammar: data.rejectedByConvertedGrammar,
      });
    });
  };

  postData = async (url, data) => {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    return response.json();
  };
}

export default Converter;
