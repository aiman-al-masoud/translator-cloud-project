from neo4j import GraphDatabase
import json

# database connection credentials
URI = "neo4j://localhost:7687"
user = "neo4j"
password = "password"

# connection with db
driver = GraphDatabase.driver(URI, auth=(user, password))

second_id = "9993"
addr = "123.123.33.321"

with driver.session() as session:
    query = """ MATCH (bad:BadTranslation)-[:IMPROVED_BY]->(good:BetterTranslation)-[:PROPOSED_BY]->(u:User)
                WHERE good.id = $second_id 
                WITH good, COUNT(u) as votes, bad
                RETURN votes, bad.id, good.id
            """
    record = session.execute_write(lambda tx, id: tx.run(query, second_id=id).data(), second_id)

    # socketio.emit('votes-update', {"secondid": record['good.second_id'], "fid": record['bad.id'], "votes": record['votes']}, brodcast=True)
    file = json.dumps({"secondid": record[0]["good.id"], "fid": record[0]["bad.id"], "votes": record[0]["votes"]})
    print(file)

driver.close()
