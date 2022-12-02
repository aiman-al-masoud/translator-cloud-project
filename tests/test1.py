from neo4j import GraphDatabase

# database connection credentials
URI = "neo4j://localhost:7687"
user = "neo4j"
password = "password"

# connection with db
driver = GraphDatabase.driver(URI, auth=(user, password))

from_text = "Hello second World!"
to_text = "Ciao grande secondo mondo!"
fid = "4567"
second_id = "4568"
addr = "4.5.6.8"

with driver.session() as session:
    query = """CREATE (:User { ip: $ip })-[:PROPOSED]->(:BetterTranslation {from_text: $from_text, to_text: $to_text, id: $id})"""
    session.execute_write(lambda tx, ip, ftx, ttx, id: tx.run(query, ip=ip, from_text=ftx, to_text=ttx, 
    id=id), addr, from_text, to_text, second_id)

    query = """MATCH (bad:BadTranslation)
            MATCH (better:BetterTranslation)
            WHERE bad.id = $fid
            MERGE (bad)-[:IMPROVED_BY]->(better)
            RETURN *
            """
    session.execute_write(lambda tx, fid: tx.run(query, fid=fid), fid)

driver.close()