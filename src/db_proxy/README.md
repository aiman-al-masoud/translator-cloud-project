# neo4j
## Some useful commands to handle the db from command line
```
MATCH (p:Person) RETURN p;
# get all "Person"
```

```
CREATE (:Person {name: "Jonny"})-[:ACTED_IN {roles: ["protagonista"]}]->(:Movie {title: "movie title", released: 1970});
# create an entity "Person" connected to another entity "Movie"
```