import json
import os
from flask import Flask, render_template

app = Flask(__name__)  # init app

LANGS = os.path.join(app.root_path, '..', 'config', 'langs.json')
langs = json.loads(open(LANGS).read())

@app.route('/')
def index():
    return render_template('index.html', langs=langs.items())


# display all records when the page "community" is loaded using the mysql's cursor for scrolling and fetching the records
@app.route('/community', methods=['GET'])
def display_records():
    return render_template('community.html')


@app.route('/about')
def about():
    return render_template('about.html')

# added for running the server directly with the run button
app.run(host='localhost', port=8082)
