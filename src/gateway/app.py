import json
import os
from flask import Flask, request, render_template, redirect
import requests

app = Flask(__name__)  # init app

LANGS = os.path.join(app.root_path, '..', 'config', 'langs.json')
langs = json.loads(open(LANGS).read())

IP_gateway="172.17.0.2"
IP_translate= "172.17.0.3"
IP_db_proxy= "172.17.0.4"
IP_db = "172.17.0.5"

@app.route('/')
def index():
    return render_template('index.html', langs=langs.items())


@app.route('/community', methods=['GET'])
def display_records():
    return render_template('community.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/translate-api', methods=['GET', 'POST'])
def translate():
    res = requests.post(f'http://${IP_translate}:8081//translate-api', json=request.json) #TODO: extract IP

    return json.dumps(res.json())


# query to the mysql db for storing the bad translation
@app.route('/query-db-api', methods=['POST', 'GET'])
def send_query():
    res = requests.post(f'http://${IP_db_proxy}:8080//insert-bad-translation', json=request.json) #TODO: extract IP

    return json.dumps(res.json())


# query to the mysql db for storing the new possible better translations
@app.route('/query-db-api2', methods=['POST', 'GET'])
def send_query2():
    res = requests.post(f'http://${IP_db_proxy}:8080//insert-possible-better-translation', json=request.json) #TODO: extract IP

    return json.dumps(res.json())


# query to the mysql db for read the bad translations
@app.route('/query-db-api3', methods=['POST', 'GET'])
def send_query3():
    res = requests.post(f'http://${IP_db_proxy}:8080//read-bad-translations', json=request.json) #TODO: extract IP

    return json.dumps(res.json())


# return all the "possibleBetterTranslation" given the id of the specific text-translation
@app.route('/query-db-api4', methods=['POST', 'GET'])
def send_query4():
    res = requests.post(f'http://${IP_db_proxy}:8080//read-possible-better-translation-by-id', json=request.json) #TODO: extract IP

    return json.dumps(res.json())


# query to the mysql db to vote a possible better translation
@app.route('/query-db-api5', methods=['POST', 'GET'])
def send_query5():
    res = requests.post(f'http://${IP_db_proxy}:8080//vote-possible-better-translation', json=request.json) #TODO: extract IP

    return json.dumps(res.json())


# added for running the server directly with the run button
app.run(host='localhost', port=5000)
