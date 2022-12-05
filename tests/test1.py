from neo4j import GraphDatabase

# database connection credentials
URI = "neo4j://localhost:7687"
user = "neo4j"
password = "password"

# connection with db
driver = GraphDatabase.driver(URI, auth=(user, password))

from_text = "Hello second World!"
to_text = "Ciao secondo mondo!"
fid = "1234"
second_id = "9999"
addr = "3.3.3.3"

with driver.session() as session:
    query = """MERGE (:BetterTranslation {from_text: $from_text, to_text: $to_text, id: $id})"""
    session.execute_write(lambda tx, ftx, ttx, id: tx.run(query, from_text=ftx, to_text=ttx,
    id=id), from_text, to_text, second_id)

    ## TODO: See if moving this at the beginning of the code
    # query = """CREATE CONSTRAINT constraint_name IF NOT EXISTS FOR (bad:BadTranslation) REQUIRE bad.id IS UNIQUE"""
    # session.execute_write(lambda tx: tx.run(query))

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

driver.close()
