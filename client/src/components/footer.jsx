import React, { Component } from "react";

class Footer extends Component {
  render() {
    return (
      <div className="py-5 text-center about">
        <div className="col-10 mx-auto text-start">
          <h5>Resources:</h5>
          <hr />
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
            <li>
              Parser is implemented using{" "}
              <a
                className="resource"
                href="https://en.wikipedia.org/wiki/Earley_parser"
                target={"_blank"}
              >
                Earley algorithm
              </a>
            </li>
          </ul>
        </div>
      </div>
    );
  }
}

export default Footer;
