from flask import Flask, render_template, request

from mapping import super_stable_matching

app = Flask(__name__)


# Transforms the preference list data (parsed from JSON) into the format expected
# by the matching solver function.
def parse_pref_list(data):
    return [[set(eq_set) for eq_set in pref_list] for pref_list in data]


# Matching solver endpoint: parse the preference lists from the input JSON,
# compute the solution, and return a JSON-compatible result dictionary
@app.route('/api/solveMatching', methods=['POST'])
def solve_matching_endpoint():
    input_g1, input_g2 = parse_pref_list(request.json['g1Prefs']), parse_pref_list(request.json['g2Prefs'])
    solution = super_stable_matching(input_g1, input_g2)
    return {'mapping': None if solution is None else list(solution)}


# Route for the index page; returns the matching demo view
@app.route('/')
def index_page():
    return render_template('matching_demo.html')


if __name__ == '__main__':
    app.run()
