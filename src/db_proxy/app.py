import json
from flask import Flask, request
from neo4j import GraphDatabase
from neo4j.exceptions import ConstraintError
from ..config.config import getConfig

app = Flask(__name__)  # init app
config = getConfig(app.root_path)

# connection with db
driver = GraphDatabase.driver(f'neo4j://{config.IP_db}:{config.neo4j_port}', auth=(config.neo4j_user, config.neo4j_password))

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

    try:
        with driver.session() as session:
            query = """
                    MERGE (b:BadTranslation { from_text: $from_text, from: $_from, to: $to, to_text: $to_text, id: $id})
                    """
            session.execute_write(lambda tx, fT, tT, ftx, ttx, id: tx.run(query, _from=fT, to=tT, from_text=ftx, to_text=ttx,
                        id=id), fromTag, toTag, from_text, to_text, _id)

            ## TODO: See if moving this at the beginning of the code
            query = """CREATE CONSTRAINT BadTranslationConstrain IF NOT EXISTS FOR (bad:BadTranslation) REQUIRE bad.id IS UNIQUE"""
            session.execute_write(lambda tx: tx.run(query))

            query = """MERGE (:User {ip: $ip})"""
            session.execute_write(lambda tx, ip: tx.run(query, ip=ip), addr)

            query = """MATCH (u:User)
                    MATCH (bad:BadTranslation)
                    WHERE bad.id = $id AND u.ip=$ip
                    MERGE (bad)-[:REPORTED_BY]->(u)
                    RETURN *
                    """
            session.execute_write(lambda tx, ip, id: tx.run(query, ip=ip, id=id), addr, _id)

    except ConstraintError as ce:
        print("ERROR: duplicated BadTranslation")
    except Exception as e:
         print("insert-bad-translation: error in the execution of the query:", e)
    finally:
        driver.close()
        return "{}"

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

    try:
        with driver.session() as session:
            query = """MERGE (:BetterTranslation {from_text: $from_text, to_text: $to_text, id: $id})"""
            session.execute_write(lambda tx, ftx, ttx, id: tx.run(query, from_text=ftx, to_text=ttx,
            id=id), from_text, to_text, second_id)

            ## TODO: See if moving this at the beginning of the code
            query = """CREATE CONSTRAINT BetterTranslationConstraint IF NOT EXISTS FOR (better:BetterTranslation) REQUIRE better.id IS UNIQUE"""
            session.execute_write(lambda tx: tx.run(query))

            query = """MERGE (:User { ip: $ip })"""
            session.execute_write(lambda tx, ip: tx.run(query, ip=ip), addr)

            query = """MATCH (u:User)
                    MATCH (better:BetterTranslation)
                    WHERE better.id = $id AND u.ip = $ip
                    MERGE (better)-[:PROPOSED_BY]->(u)
                    RETURN *
                    """
            session.execute_write(lambda tx, ip, id: tx.run(query, ip=ip, id=id), addr, second_id)

            query = """MATCH (bad:BadTranslation)
                    MATCH (better:BetterTranslation)
                    WHERE bad.id = $fid
                    MERGE (bad)-[:IMPROVED_BY]->(better)
                    RETURN *
                    """
            session.execute_write(lambda tx, fid: tx.run(query, fid=fid), fid)

    except ConstraintError as ce:
        print("ERROR: duplicated BetterTranslation")
    except Exception as e:
        print('/insert-possible-better-translation: error in the execution of the query')
    finally:
        driver.close()
        return "{}"
    #TODO: counts the number of votes for each better translation


@app.route('/read-bad-translations', methods=['POST', 'GET'])
def read_bad_translations():

    '''query to the mysql db to read the bad translations'''

    if request.method == 'POST':
        page =  request.json['page']

        try:
            with driver.session() as session:
                query = """ MATCH (b:BadTranslation)-[:REPORTED_BY]->(u:User)
                    WITH b, count(u) as complaints
                    RETURN *
                    ORDER BY complaints DESC
                    SKIP $page*$offset
                    LIMIT $offset
                    """
                result = session.execute_read(lambda tx, page, offset: tx.run(query, page=page, offset=offset).data(), page, OFFSET)
        except Exception as e:
            print('/read-bad-translations: error in the execution of the query')
        finally:
            driver.close()

    matched_bad_translations = list()
    for record in result:
        b = record["b"]
        b.update({'complaints': record['complaints']})
        matched_bad_translations.append(b)
    return json.dumps(matched_bad_translations)

@app.route('/read-possible-better-translation-by-id', methods=['POST', 'GET'])
def read_possible_better_translation_by_id():

    '''return all the "possibleBetterTranslation" given the id of the specific text-translation'''

    if request.method == 'POST':
        id_prop =  (int)(request.json['id_prop'])
        page =  request.json['page']
    try:
        with driver.session() as session:
            query = """ MATCH (bad:BadTranslation)-[:IMPROVED_BY]->(good:BetterTranslation)-[:PROPOSED_BY]->(u:User)
                        WHERE bad.id = $id_prop
                        WITH good, COUNT(u) as votes
                        RETURN *
                        ORDER BY votes DESC
                        SKIP $page*$offset
                        LIMIT $offset
                    """
            result = session.execute_read(lambda tx, page, offset, id_prop: tx.run(query, page=page, offset=offset, id_prop=id_prop).data(), page, OFFSET, id_prop)
    except Exception as e:
        print('/read-possible-better-translation-by-id: error in the execution of the query')
    finally:
        driver.close()

    matched_possible_better_translations = list()
    for record in result:
        pb = record["good"]
        pb.update({'votes': record['votes']})
        matched_possible_better_translations.append(pb)
    return json.dumps(matched_possible_better_translations)

@app.route('/vote-possible-better-translation', methods=['POST', 'GET'])
def vote_possible_better_translation():

    '''query to the mysql db to vote a possible better translation'''

    if request.method == 'POST':
        second_id = int(request.json['secondid'])
        # operation = request.json["operation"] ## TODO: remove it??
        addr = request.json["ip"]

    try:
        with driver.session() as session:
            query = """MERGE (:User {ip: $ip})"""
            session.execute_write(lambda tx, ip: tx.run(query, ip=ip), addr)

            ## TODO: add constrain on the user, the one who proposes the translation should not be the one who votes

            query = """MATCH (u:User)
                    MATCH (better:BetterTranslation)
                    WHERE better.id = $id AND u.ip = $ip
                    MERGE (better)-[:PROPOSED_BY]->(u)
                    RETURN *
                    """
            # a vote to a BetterTranslation is mapped with a PROPOSED_BY relation (link)
            session.execute_write(lambda tx, id, ip: tx.run(query, id=id, ip=ip), second_id, addr)
           

            query = """ MATCH (bad:BadTranslation)-[:IMPROVED_BY]->(good:BetterTranslation)-[:PROPOSED_BY]->(u:User)
                        WHERE good.id = $second_id 
                        WITH good, COUNT(u) as votes, bad
                        RETURN votes, bad.id, good.id
                    """

            record = session.execute_read(lambda tx, id: tx.run(query, second_id=id).data(), second_id)
            data = json.dumps({"secondid": record[0]["good.id"], "fid": record[0]["bad.id"], "votes": record[0]["votes"]})
            print(data)
            return data
            
    except Exception as e:
        print('/vote_possible_better_translation: error in the execution of the query')
        print(e)
    finally:
        driver.close()

# added for running the server directly with the run button
app.run(host=config.host, port=config.db_proxy_port)