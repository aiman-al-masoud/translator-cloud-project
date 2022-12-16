from neo4j import GraphDatabase
from neo4j.exceptions import ConstraintError

# database connection credentials
URI = "neo4j://localhost:7687"
user = "neo4j"
password = "password"

# connection with db
driver = GraphDatabase.driver(URI, auth=(user, password))

'''query to the db for storing the bad translation'''

fromTag = "it"
toTag = "en"
from_text = "Hello World 999!"
to_text = "Ciao mondo 999!"
_id = "999"
addr = "9.9.9.9"

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
