#!/bin/python3

from neo4j import GraphDatabase
from progress.bar import Bar
from neo4j.exceptions import ConstraintError
import argparse

# database connection credentials
URI = "neo4j://localhost:7687"
user = "neo4j"
password = "password"

# connection with db
driver = GraphDatabase.driver(URI, auth=(user, password))

def storeBadTranslation(from_text, to_text, _id, addr, fromTag="it", toTag="en"):    
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

def storeBetterTranslation(from_text, to_text, second_id, fid, addr, fromTag="it", toTag="en"):
    try:
        with driver.session() as session:
                query = """MERGE (:BetterTranslation {from_text: $from_text, to_text: $to_text, id: $id})"""
                session.execute_write(lambda tx, ftx, ttx, id: tx.run(query, from_text=ftx, to_text=ttx,
                id=id), from_text, to_text, second_id)

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

def votesBetterTranslation(addr, second_id):
    try:
        with driver.session() as session:
            query = """MERGE (:User {ip: $ip})"""
            session.execute_write(lambda tx, ip: tx.run(query, ip=ip), addr)

            query = """MATCH (u:User)
                    MATCH (better:BetterTranslation)
                    WHERE better.id = $id AND u.ip=$ip
                    MERGE (better)-[:PROPOSED_BY]->(u)
                    RETURN *
                    """
            # a vote to a BetterTranslation is mapped with a PROPOSED_BY relation (link)
            session.execute_write(lambda tx, id, ip: tx.run(query, id=id, ip=ip), second_id, addr)
            
    except Exception as e:
        print('/votes-possible-better-translation-by-id: error in the execution of the query')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = 'fillDB.py',
        description = 'Script useful to automatically fill the neo4j database',
        )
    parser.add_argument("--number", "-n", default=10, help='number of "things" to do in the database')
    parser.add_argument("--empytDB", "-e", choices=['y', 'n'], default='y', help='decide whether empyt the database or not')

    args = parser.parse_args()

    print("Automatic database filling\n\t === \t")
    
    if args.empytDB == 'y':
        with driver.session() as session:
            query = """MATCH (n) DETACH DELETE n"""
            session.execute_write(lambda tx: tx.run(query))
            print("Database deleted!")

    with Bar('Bad-Translations', max=int(args.number), suffix='%(percent)d%%') as bar:
        for bad in range(int(args.number)):
            ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0,255),4)) # not sure of what it does, but it works..
            if bad % 2 > 0:
                storeBadTranslation(f"Ciao {bad-1} mondo!", f"Hello {bad-1} world!", bad-1, ip)# claim
            else:
                storeBadTranslation(f"Ciao {bad} mondo!", f"Hello {bad} world!", bad, ip)# inserted
            bar.next()
    
    with Bar('Better-Translations', max=int(args.number)/2, suffix='%(percent)d%%') as bar:
        for better in range(0,int(args.number),2):
            ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0,255),4)) # not sure of what it does, but it works..
            storeBetterTranslation(f"Ciao {better} mondo!", f"Hello {better} world better!", better*2, better, ip)
            bar.next()
    
    with Bar('Votes Better-Translations', max=int(args.number)/2, suffix='%(percent)d%%') as bar:
        for votes in range(0,int(args.number),2):
            ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0,255),4)) # not sure of what it does, but it works..
            votesBetterTranslation(ip, 2*votes)
            bar.next()
    
