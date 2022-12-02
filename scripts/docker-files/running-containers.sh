#!/bin/bash
docker build --tag translator_gateway ./gateway
docker build --tag translator_translate ./translate
docker build --tag translator_db_proxy ./db_proxy

docker stop translator_gateway_container
docker stop translator_translate_container
docker stop translator_db_proxy_container

docker rm translator_gateway_container
docker rm translator_translate_container
docker rm translator_db_proxy_container

docker run -d -it -p 5000:5000 --name translator_gateway_container translator_gateway
sleep 2
docker run -d -it --name translator_translate_container translator_translate
sleep 2
docker run -d -it --name translator_db_proxy_container translator_db_proxy
