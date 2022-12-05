from neo4j import GraphDatabase
import json

# database connection credentials
URI = "neo4j://localhost:7687"
user = "neo4j"
password = "password"

# connection with db
driver = GraphDatabase.driver(URI, auth=(user, password))

page = 0;
OFFSET = 2;

with driver.session() as session:
    query = """ MATCH (bad:BadTranslation)-[:IMPROVED_BY]->(good:BetterTranslation)-[:VOTED_BY]->(u:User)
                WITH good, COUNT(u) as votes
                RETURN { from_text: good.from_text , to_text: good.to_text , id: good.id , votes: votes}
                SKIP $page*$offset
                LIMIT $offset
            """
    result = session.execute_read(lambda tx, page, offset: list(tx.run(query, page=page, offset=offset)), page, OFFSET)
driver.close()
    print(json.dumps(result))
