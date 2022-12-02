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
```bash
docker run -d --name translator_db_container -e TZ=UTC -p 30306:3306 -e MYSQL_ROOT_PASSWORD=My:S3cr3t/ translator_db
```
To link the local terminal with the one of the docker container:
```bash
docker exec -it translator_db_container bash
```
Once you are inside the docker container initiate the database with the following command:
``` bash
echo "source init-db.sql" | mysql -u root -p"My:S3cr3t/"
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
