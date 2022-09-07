from flask import Flask, request

from chomsky import Chomsky
from greibach import Greibach
from parser import Parser
from grammar import Grammar

app = Flask(__name__)

CHOMSKY = 1
GREIBACH = 2


@app.route("/convert", methods=["POST"])
def convert():
    request_data = request.get_json()
    grammar = Grammar(request_data['grammar'])
    conversion_form = int(request_data['conversionForm'])

    converter = None
    if conversion_form == CHOMSKY:
        converter = Chomsky(grammar)
    elif conversion_form == GREIBACH:
        converter = Greibach(grammar)

    converted_grammar = converter.convert()

    return {
        "convertedGrammar": converted_grammar.rules,
        "conversionMessages": converter.messages
    }


@app.route("/test", methods=["POST"])
def test():
    request_data = request.get_json()
    string = request_data['string']
    grammar = Grammar(request_data['grammar'])
    result_grammar = Grammar(request_data['resultGrammar'])

    derives_from_original_grammar = Parser(grammar).check_drives_from_grammar(string)
    derives_from_converted_grammar = Parser(result_grammar).check_drives_from_grammar(string)
    return {
        "isDerivedFromOriginalGrammar": derives_from_original_grammar,
        "isDerivedFromResultGrammar": derives_from_converted_grammar
    }


if __name__ == "__main__":
    app.run(debug=True, port=4999)
