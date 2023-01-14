import React, { Component } from "react";

class About extends Component {
  render() {
    return (
      <div className="py-5 text-center about">
        <div className="col-8 mx-auto">
          <h1>CFG Converter</h1>
          <div className="text-start">
            <hr />
            <p>
              This website is a tool that converts input context-free grammar to
              different normal forms. Currently, we support following forms:{" "}
              <br />
            </p>
            <ul>
              <li>
                <a
                  className="resource"
                  href="https://en.wikipedia.org/wiki/Chomsky_normal_form"
                  target={"_blank"}
                >
                  Chomsky normal form (CNF)
                </a>
              </li>
              <li>
                <a
                  className="resource"
                  href="https://en.wikipedia.org/wiki/Greibach_normal_form"
                  target={"_blank"}
                >
                  Greibach normal form (GNF)
                </a>
              </li>
            </ul>
            <p>
              Before conversion, the grammar gets simplified and redundant rules
              (such as null and unit productions) are deleted.
            </p>
            <h5>Resources:</h5>
            <ul>
              <li>
                <a
                  className="resource"
                  href="https://www.amazon.com/Formal-Languages-Compilation-Computer-Science/dp/3030048780"
                  target={"_blank"}
                >
                  Formal Languages and Compilation (3rd Edition)
                </a>
                , Authors: Stefano Crespi Reghizzi, Luca Breveglieri, Angelo
                Morzenti
              </li>
              <li>
                <a
                  className="resource"
                  href="https://www.youtube.com/playlist?list=PLBlnK6fEyqRgp46KUv4ZY69yXmpwKOIev"
                  target={"_blank"}
                >
                  Theory of computation and automata
                </a>
                , Neso Academy
              </li>
            </ul>
          </div>
        </div>
      </div>
    );
  }
}

export default About;
