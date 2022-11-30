*The following commands must be run after having docker installed*

# Building and executing containers which enclose the various components of the application

## Building the image which will be responsible of the database behaviour
Place yourself inside the directory **db**, then execute:
```bash
docker build --tag translator_db .
```

## Building the image which will be responsible of the gateway behaviour
Place yourself inside the directory **gateway**, then execute:
```bash
docker build --tag translator_gateway .
```

*To run the following commands it is not necessary to place yourself in a specific directory*
## Running the translator_db image

### First time
```bash
docker run -d --name mysql -e TZ=UTC -p 30306:3306 -e MYSQL_ROOT_PASSWORD=My:S3cr3t/ translator_db
```

### Followitng times
After the first usage it is possible to run always the same container without creating a new one from the image
```bash
docker start translator_db_container
```

### Use the container
To link the local terminal with the one of the docker container:
```bash
docker exec -it translator_db_container bash
```

``` bash
echo "source init-db.sql" | mysql -u root -p"My:S3cr3t/"
```

## Running the translator_gateway image
### First time
```bash
docker run -d -it --name translator_gateway_container translator_gateway
```

### Followitng times
After the first usage it is possible to run always the same container without creating a new one from the image
```bash
docker start translator_gateway_container
```

### Use the container
To link the local terminal with the one of the docker container:
```bash
docker exec -it translator_gateway_container bash
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
```
