from neo4j import GraphDatabase

# database connection credentials
URI = "neo4j://localhost:7687"
user = "neo4j"
password = "password"

# connection with db
driver = GraphDatabase.driver(URI, auth=(user, password))

second_id = "9999"
addr = "8.8.8.8"

with driver.session() as session:
    query = """MERGE (:User {ip: $ip})"""
    session.execute_write(lambda tx, ip: tx.run(query, ip=ip), addr)

    ## TODO: add constrain on the user, the one who proposes the translation should not be the one who votes

    query = """MATCH (u:User)
            MATCH (better:BetterTranslation)
            WHERE better.id = $id AND u.ip=$ip
            MERGE (better)-[:VOTED_BY]->(u)
            RETURN *
            """
    session.execute_write(lambda tx, id, ip: tx.run(query, id=id, ip=ip), second_id, addr)

driver.close()
