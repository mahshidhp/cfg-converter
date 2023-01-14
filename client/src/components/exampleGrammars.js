const exampleGrammars = [
  //example 1
  [
    { lhs: "S", rhs: ["ASA", "aB"] },
    { lhs: "A", rhs: ["B", "S"] },
    { lhs: "B", rhs: ["b", "ε"] },
  ],
  //example 2
  [
    { lhs: "S", rhs: ["F", "SQS"] },
    { lhs: "F", rhs: ["x"] },
    { lhs: "Q", rhs: ["+", "*"] },
  ],
  //example 3
  [
    { lhs: "", rhs: [""] },
    { lhs: "", rhs: [""] },
    { lhs: "", rhs: [""] },
    { lhs: "", rhs: [""] },
  ],
];

export default exampleGrammars;
