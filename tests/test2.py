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
                    RETURN *
                    ORDER BY complaints DESC
                    SKIP $page*$offset
                    LIMIT $offset
                    """
            result = session.execute_read(lambda tx, page, offset: (tx.run(query, page=page, offset=offset)).data(), page, OFFSET)
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

print(functionTest())
