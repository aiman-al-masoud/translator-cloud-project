*The following commands must be run after having docker installed*

# Building and executing containers which enclose the various components of the application
## Building the image which will be responsible of the gateway behaviour
Place yourself inside the directory **gateway**, then execute:
```bash
docker build --tag translator_gateway .
```

## Building the image which will be responsible of the translation behaviour
Place yourself inside the directory **translate**, then execute:
```bash
docker build --tag translator_translate .
```

## Building the image which will be responsible of the proxy-database behaviour
Place yourself inside the directory **db_proxy**, then execute:
```bash
docker build --tag translator_db_proxy .
```

## Building the image which will be responsible of the database behaviour
Place yourself inside the directory **db**, then execute:
```bash
docker build --tag translator_db .
```

*To run the following commands it is not necessary to place yourself in a specific directory*
## Running the images for the first time
```bash
docker run -d -it -p 5000:5000 --name translator_gateway_container translator_gateway
```
```bash
docker run -d -it --name translator_translate_container translator_translate
```
```bash
docker run -d -it --name translator_db_proxy_container translator_db_proxy
```

The last to be started is the database
```sh
docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data neo4j
```

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

## Exiting containers
From inside the container:
```bash
exit
```

## Stopping containers
```bash
docker stop translator_db_container
docker stop translator_gateway_container
docker stop translator_db_proxy_container
docker stop translator_translate_container
```

## IP
These are the IPs used by the containers:
-   **translator_gateway**: 172.17.0.2 -- `5000`
-   **translator_translate**: 172.17.0.3 -- `8081`
-   **translator_db_proxy**: 172.17.0.4 -- `8080`
-   **translator_db**: 172.17.0.5
