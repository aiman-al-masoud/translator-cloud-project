from neo4j import GraphDatabase
import json

# database connection credentials
URI = "neo4j://localhost:7687"
user = "neo4j"
password = "password"

# connection with db
driver = GraphDatabase.driver(URI, auth=(user, password))

page = 0
OFFSET = 3

def functionTest():
    try:
        with driver.session() as session:
            query = """ MATCH (b:BadTranslation)-[:REPORTED_BY]->(u:User)
                    WITH b, count(u) as complaints
                    RETURN { from_tag: b.from , to_tag: b.to , from_text: b.from_text , to_text: b.to_text , id: b.id, complaints: complaints }
                    ORDER BY complaints DESC
                    SKIP $page*$offset
                    LIMIT $offset
                    """
            result = session.execute_read(lambda tx, page, offset: list(tx.run(query, page=page, offset=offset)), page, OFFSET)
    except Exception as e:
        print('/read-bad-translations: error in the execution of the query')
    finally:
        driver.close()

    return json.dumps(result)


print(functionTest())