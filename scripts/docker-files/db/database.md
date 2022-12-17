# neo4j db server
To run the db use the following command:
```sh
docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data neo4j
```

## Login
For the first time login with
```
    user = "neo4j"
    password = "neo4j"
```
then change the password with
```
    user = "neo4j"
    password = "password"
```

## To use the db from command line
```sh
cypher-shell
```

## Browser interface
```
http://localhost:7474/ 
```

## Empty database
```
MATCH (n) DETACH DELETE n
```