from flask import Flask, request, send_from_directory, make_response
from flask_cors import CORS, cross_origin

from converter.Chomsky import Chomsky
from converter.Greibach import Greibach
from converter.Parser import Parser
from converter.Grammar import Grammar
from converter.Exceptions import *
from converter.TestcaseGenerator import TestcaseGenerator

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
            raise FormNotSelected("No conversion form is selected.")

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
            "errorMessage": "",
        }

    except (FormNotSelected, GrammarIsNotCFG) as e:
        return {
            "errorMessage": str(e),
            "simplificationTimeline": [],
            "simplificationMessages": [],
            "convertedGrammar": [],
        }


@app.route("/test", methods=["POST"])
@cross_origin()
def test():
    request_body = request.get_json()
    string = request_body['string']
    grammar = Grammar(request_body['grammar'])
    result_grammar = Grammar(request_body['resultGrammar'])

    derives_from_original_grammar = Parser(grammar, string).parse()
    derives_from_converted_grammar = Parser(result_grammar, string).parse()
    return {
        "isDerivedFromOriginalGrammar": derives_from_original_grammar,
        "isDerivedFromResultGrammar": derives_from_converted_grammar
    }


@app.route("/examples", methods=["POST"])
@cross_origin()
def generate_example_word():
    request_body = request.get_json()
    count = request_body['count'] or 5
    original_grammar = Grammar(request_body['grammar'])
    result_grammar = Grammar(request_body['resultGrammar'])
    original_grammar_examples = original_grammar.generate_example_words(count)
    result_grammar_examples = result_grammar.generate_example_words(count)
    return {
        "originalGrammarExamples": original_grammar_examples,
        "resultGrammarExamples": result_grammar_examples
    }


@app.route("/testcase", methods=["POST"])
@cross_origin()
def generate_testcase():
    request_body = request.get_json()
    count = request_body['count'] or 5
    original_grammar = Grammar(request_body['grammar'])
    result_grammar = Grammar(request_body['resultGrammar'])

    result = TestcaseGenerator(original_grammar, result_grammar).generate(count)
    acc_by_grammar1, rej_by_grammar1, acc_by_grammar2, rej_by_grammar2 = result

    return {
        "acceptedByOriginalGrammar": acc_by_grammar1,
        "rejectedByOriginalGrammar": rej_by_grammar1,
        "acceptedByConvertedGrammar": acc_by_grammar2,
        "rejectedByConvertedGrammar": rej_by_grammar2
    }


@app.route("/")
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(debug=True, port=4999)
