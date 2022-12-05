from neo4j import GraphDatabase
from neo4j.exceptions import ConstraintError

# database connection credentials
URI = "neo4j://localhost:7687"
user = "neo4j"
password = "password"

# connection with db
driver = GraphDatabase.driver(URI, auth=(user, password))

from_text = "Hello World 555!"
to_text = "Ciao mondo molto bello!"
fid = "3333"
second_id = "33514"
addr = "11.33.11.14"

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
                    WHERE bad.id = $fid AND better.id = $second_id
                    MERGE (bad)-[:IMPROVED_BY]->(better)
                    RETURN *
                    """
            session.execute_write(lambda tx, fid, second_id: tx.run(query, fid=fid, second_id=second_id), fid, second_id)
            
except ConstraintError as ce:
    print("ERROR: duplicated BetterTranslation")
except Exception as e:
    print('/insert-possible-better-translation: error in the execution of the query')
finally:
    driver.close()
#TODO: counts the number of votes for each better translation
