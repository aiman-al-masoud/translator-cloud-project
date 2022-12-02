import json
import os
from flask import Flask, request
from neo4j import GraphDatabase

app = Flask(__name__)  # init app

# database connection credentials
URI = "neo4j://localhost:7687"
user = "neo4j"
password = "password"

# connection with db
driver = GraphDatabase.driver(URI, auth=(user, password))

OFFSET = 2

def check_json(request):
    if request.json is None:
        return 'error: must include json in request', 400

    for k in ['from', 'to', 'from_text', 'id']:
        if k not in request.json:
            return f'error: missing {k} in json', 400

    if not request.json['from_text'].strip():
        return 'error: empty requested translation', 400

    return 1

@app.route('/insert-bad-translation', methods=['POST', 'GET'])
def insert_bad_translation():
    '''query to the db for storing the bad translation'''

    if (check:=check_json(request)) != 1:
        return check

    if request.method == 'POST':
        fromTag = request.json['from']
        toTag = request.json['to']
        from_text = request.json['from_text']
        to_text = request.json['to_text']
        _id = request.json['id']
        addr = request.remote_addr

        # avoiding to send the response with error 500 (since there is already an equal request saved in the database)
        # users will see "Thank you for your feedback" regardless

    with driver.session() as session:
        query = """CREATE (:User { ip: $ip })-[:REPORTED]->
                (:BadTranslation { from: $_from, to: $to, from_text: $from_text, to_text: $to_text, from_text: $from_text, id: $id}) 
                """
        session.execute_write(lambda tx, ip, fT, tT, ftx, ttx, id: tx.run(query, ip=ip, _from=fT, to=tT, from_text=ftx, to_text=ttx, 
                id=id), addr, fromTag, toTag, from_text, to_text, _id)

    driver.close()

@app.route('/insert-possible-better-translation', methods=['POST', 'GET'])
def insert_possible_better_translation():

    '''query to the mysql db for storing the new possible better translations'''

    if request.method == 'POST':
        from_text = request.json['from_text']
        to_text = request.json['to_text']
        fid = request.json['fid']
        second_id = request.json['secondid']
        addr = request.remote_addr

        if(not from_text.strip() or not to_text.strip()):
            return "Empty from_text or to_text", 400

        # avoiding to send the response with error 500 (since there is already an equal request saved in the database)
        # users will see "Thank you for your feedback" regardless
    
    with driver.session() as session:
        query = """CREATE (:User { ip: $ip })-[:PROPOSED]->(:BetterTranslation {from_text: $from_text, to_text: $to_text, id: $id});
                    MATCH (bad:BadTranslation)
                    MATCH (better:BetterTranslation)
                    WHERE bad.id = $fid
                    MERGE (bad)-[:IMPROVED_BY]->(better)
                    RETURN *
                """
        session.execute_write(lambda tx, ip, ftx, ttx, id, fid: tx.run(query, ip=ip, from_text=ftx, to_text=ttx, 
            id=id, fid=fid), addr, from_text, to_text, second_id, fid)
    #TODO: counts the number of votes for each better translation
    driver.close()

@app.route('/read-bad-translations', methods=['POST', 'GET'])
def read_bad_translations():

    '''query to the mysql db to read the bad translations'''

    if request.method == 'POST':
        page =  request.json['page']
    
    #TODO
    pass

@app.route('/read-possible-better-translation-by-id', methods=['POST', 'GET'])
def read_possible_better_translation_by_id():

    '''return all the "possibleBetterTranslation" given the id of the specific text-translation'''

    if request.method == 'POST':
        id_prop =  request.json['id_prop']
        page =  request.json['page']
    
    #TODO
    pass

@app.route('/vote-possible-better-translation', methods=['POST', 'GET'])
def vote_possible_better_translation():

    '''query to the mysql db to vote a possible better translation'''

    if request.method == 'POST':
        second_id = request.json['secondid']
        operation = request.json["operation"]
    
    #TODO
    pass

# added for running the server directly with the run button
app.run(host='localhost', port=8080)