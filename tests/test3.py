from neo4j import GraphDatabase
import json

# database connection credentials
URI = "neo4j://localhost:7687"
user = "neo4j"
password = "password"

# connection with db
driver = GraphDatabase.driver(URI, auth=(user, password))

page = 0
OFFSET = 5
id_prop = "555"

def functionTest():
    try:
        with driver.session() as session:
            query = """ MATCH (bad:BadTranslation)-[:IMPROVED_BY]->(good:BetterTranslation)-[:PROPOSED_BY]->(u:User)
                        WHERE bad.id = $id_prop
                        WITH good, COUNT(u) as votes
                        RETURN { from_text: good.from_text , to_text: good.to_text , id: good.id , votes: votes}
                        ORDER BY votes DESC
                        SKIP $page*$offset
                        LIMIT $offset
                    """
            result = session.execute_read(lambda tx, page, offset, id_prop: list(tx.run(query, page=page, offset=offset, id_prop=id_prop)), page, OFFSET, id_prop)

    except Exception as e:
        print('/read-possible-better-translation-by-id: error in the execution of the query')
    finally:
        driver.close()

    return json.dumps(result)

print(functionTest())
