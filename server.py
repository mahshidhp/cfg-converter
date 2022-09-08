from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin

from chomsky import Chomsky
from greibach import Greibach
from grammarParser import GrammarParser
from grammar import Grammar

app = Flask(__name__, static_folder="client/build", static_url_path="")
CORS(app)

CHOMSKY = 1
GREIBACH = 2


@app.route("/convert", methods=["POST"])
@cross_origin()
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
@cross_origin()
def test():
    request_data = request.get_json()
    string = request_data['string']
    grammar = Grammar(request_data['grammar'])
    result_grammar = Grammar(request_data['resultGrammar'])

    derives_from_original_grammar = GrammarParser(grammar).check_drives_from_grammar(string)
    derives_from_converted_grammar = GrammarParser(result_grammar).check_drives_from_grammar(string)
    return {
        "isDerivedFromOriginalGrammar": derives_from_original_grammar,
        "isDerivedFromResultGrammar": derives_from_converted_grammar
    }


@app.route("/")
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(debug=False, port=4999)
