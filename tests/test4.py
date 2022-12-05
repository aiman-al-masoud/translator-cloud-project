from neo4j import GraphDatabase

# database connection credentials
URI = "neo4j://localhost:7687"
user = "neo4j"
password = "password"

# connection with db
driver = GraphDatabase.driver(URI, auth=(user, password))

second_id = "55513"
addr = "123.123.33.321"

with driver.session() as session:
    query = """MERGE (:User {ip: $ip})"""
    session.execute_write(lambda tx, ip: tx.run(query, ip=ip), addr)

    ## TODO: add constrain on the user, the one who proposes the translation should not be the one who votes

    query = """MATCH (u:User)
            MATCH (better:BetterTranslation)
            WHERE better.id = $id AND u.ip=$ip
            MERGE (better)-[:PROPOSED_BY]->(u)
            RETURN *
            """
    # a vote to a BetterTranslation is mapped with a PROPOSED_BY relation (link)
    session.execute_write(lambda tx, id, ip: tx.run(query, id=id, ip=ip), second_id, addr)

driver.close()
