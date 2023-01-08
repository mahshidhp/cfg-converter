from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin

from converter.Chomsky import Chomsky
from converter.Greibach import Greibach
from converter.GrammarParser import EarleyParser
from converter.Grammar import Grammar

app = Flask(__name__, static_folder="client/build", static_url_path="")
CORS(app)

CHOMSKY = 1
GREIBACH = 2


@app.route("/convert", methods=["POST"])
@cross_origin()
def convert():
    try:
        request_body = request.get_json()
        grammar = Grammar(request_body['grammar'])

        if request_body['conversionForm']:
            conversion_form = int(request_body['conversionForm'])
        else:
            raise Exception("No conversion form is selected.")

        converter = None
        if conversion_form == CHOMSKY:
            converter = Chomsky(grammar)
        elif conversion_form == GREIBACH:
            converter = Greibach(grammar)

        converter.convert()

        return {
            "simplificationTimeline": [grammar.get_json_compact_rules() for grammar in converter.simplifier.grammar_timeline],
            "simplificationMessages": converter.simplifier.messages,
            "convertedGrammar": converter.grammar.get_json_compact_rules(),
            "conversionMessages": converter.messages,
            "errorMessage": "",
        }

    except Exception as e:
        return {
            "errorMessage": str(e),
            "simplificationTimeline": [],
            "simplificationMessages": [],
            "convertedGrammar": [],
            "conversionMessages": []
        }


@app.route("/test", methods=["POST"])
@cross_origin()
def test():
    request_body = request.get_json()
    string = request_body['string']
    grammar = Grammar(request_body['grammar'])
    result_grammar = Grammar(request_body['resultGrammar'])

    derives_from_original_grammar = EarleyParser(string, grammar).run()
    derives_from_converted_grammar = EarleyParser(string, result_grammar).run()
    return {
        "isDerivedFromOriginalGrammar": derives_from_original_grammar,
        "isDerivedFromResultGrammar": derives_from_converted_grammar
    }


@app.route("/")
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(debug=True, port=4999)
