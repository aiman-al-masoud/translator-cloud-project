from neo4j import GraphDatabase

# database connection credentials
URI = "neo4j://localhost:7687"
user = "neo4j"
password = "password"

# connection with db
driver = GraphDatabase.driver(URI, auth=(user, password))

'''query to the db for storing the bad translation'''

fromTag = "it"
toTag = "en"
from_text = "Hello second World!"
to_text = "Ciao secondo mondo!"
_id = "4567"
addr = "4.5.6.7"
    
with driver.session() as session:
    query = """CREATE (:User { ip: $ip })-[:REPORTED]->
            (:BadTranslation { from_text: $from_text, from: $_from, to: $to, to_text: $to_text, from_text: $from_text, id: $id}) 
            """
    session.execute_write(lambda tx, ip, fT, tT, ftx, ttx, id: tx.run(query, ip=ip, _from=fT, to=tT, from_text=ftx, to_text=ttx, 
            id=id), addr, fromTag, toTag, from_text, to_text, _id)

driver.close()